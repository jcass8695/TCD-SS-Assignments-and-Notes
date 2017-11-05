import socket
import sys
import threading
from protocol_responses import *
from protocol_messages import *
from client import Client
from chatroom import Chatroom

HOST = sys.argv[1]
JOIN_PORT = 3000
BUFFER_SIZE = 4096
BACKLOG = 5
# Map of join_id's to Client objects
CLIENTS_MAP = {}

# Map of room_id's to Chatroom objects
CHATROOMS_MAP = {}


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Prevent OSError 98: Address already in use (TCP TIME_WAIT)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, JOIN_PORT))
    server_socket.listen(BACKLOG)
    print("Main Server Thread Listening")

    while True:
        try:
            # New Join request
            new_client_sock, new_client_addr = server_socket.accept()
            print("New join request from {}".format(new_client_addr))
            threading.Thread(
                target=client_thread,
                args=(new_client_sock, new_client_addr)
            ).start()

        except Exception as e:
            print("Exception on server")
            print(e)
            break

    server_socket.close()
    print("Server shutting down")


def client_thread(client_socket, client_address):
    client = None
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode()
            if message:
                print("Server received:\n{}".format(message))
                if check_hello(message):
                    process_helo_req(client_socket, message)

                elif check_kill(message):
                    print("Killing server")
                    sys.exit()

                elif check_join(message):
                    # Create new Client object
                    if client is None:
                        client = new_client_setup(
                            message,
                            client_socket,
                            client_address
                        )

                    process_join_req(client, message)

                elif check_leave(message):
                    process_leave_req(client, message)

                elif check_message(message):
                    process_message_req(client, message)

                elif check_disconnect(message):
                    print(CHATROOMS_MAP)
                    process_disconnect_req(client, message)
                    break

            else:
                print("Client closed connection unexpectedly")
                # process_disconnect_req(client, message)
                break

        except Exception as e:
            print(e.with_traceback())
            break

    client_socket.close()


def new_client_setup(join_req, client_socket, client_address):
    _, client_name = parse_join(join_req)
    join_id = hash(client_name) % 255
    return Client(
        client_name,
        join_id,
        client_socket,
        client_address
    )


def process_helo_req(client_socket, message):
    client_socket.sendall(respond_to_hello(message, HOST))


def process_join_req(client, message):
    room_name, _ = parse_join(message)
    room_id = hash(room_name) % 255
    if room_id not in CHATROOMS_MAP.keys():
        CHATROOMS_MAP[room_id] = Chatroom(room_id, room_name)

    if CHATROOMS_MAP[room_id].add_client(client):
        client.socket.sendall(respond_to_join(
            room_name,
            room_id,
            client.join_id,
            HOST,
            client.address[1]
        ))

        CHATROOMS_MAP[room_id].broadcast_message(
            client.handle,
            "{} Joined {}".format(client.handle, CHATROOMS_MAP[room_id].room_name)
        )

    else:
        client.socket.sendall(respond_with_error(1))


def process_leave_req(client, message):
    room_id, join_id = parse_leave(message)
    if room_id not in CHATROOMS_MAP.keys():
        client.socket.sendall(respond_with_error(2))
        return

    elif join_id != client.join_id:
        client.socket.sendall(respond_with_error(3))
        return

    client.socket.sendall(respond_to_leave(room_id, client.join_id))
    CHATROOMS_MAP[room_id].broadcast_message(
        client.handle,
        "{} Left {}".format(client.handle, CHATROOMS_MAP[room_id].room_name)
    )

    CHATROOMS_MAP[room_id].remove_client(client)

def process_message_req(client, message):
    room_id, join_id, message_text = parse_message(message)
    if room_id not in CHATROOMS_MAP.keys():
        client.socket.sendall(respond_with_error(2))
        return

    elif join_id not in CHATROOMS_MAP[room_id].connected_clients.keys():
        client.socket.sendall(respond_with_error(4))
        return

    CHATROOMS_MAP[room_id].broadcast_message(
        client.handle,
        message_text
    )


def process_disconnect_req(client, message):
    client_name = parse_disconnect(message)
    if client_name is not client.handle:
        client.socket.sendall(respond_with_error(5))
        return

    # Remove client from all of it's connected chatrooms
    for _, chatroom in CHATROOMS_MAP.items():
        print(chatroom.room_name)
        chatroom.remove_client(client)


if __name__ == "__main__":
    run()
