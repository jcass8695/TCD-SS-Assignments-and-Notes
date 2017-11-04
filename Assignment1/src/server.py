import socket
import select
import threading
from protocol_responses import *
from protocol_messages import *
from client import Client
from chatroom import Chatroom

HOST = "127.0.0.1"
JOIN_PORT = 3000
BUFFER_SIZE = 4096

# Map of join_id's to Client objects
CLIENTS_MAP = {}

# Map of room_id's to Chatroom objects
CHATROOMS_MAP = {}


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Prevent OSError 98: Address already in use (TCP TIME_WAIT)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, JOIN_PORT))
    server_socket.listen()
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
    # Create new Client object
    client = new_client_setup(client_socket, client_address)
    while True:
        try:
            message = client.socket.recv(BUFFER_SIZE).decode()
            if message:
                print("Server received:\n{}".format(message))
                if check_join(message):
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
                process_disconnect_req(client, message)
                break

        except Exception as e:
            print(e)
            break

    client_socket.close()


def new_client_setup(client_socket, client_address):
    join_req = client_socket.recv(BUFFER_SIZE).decode()
    if check_join(join_req):
        room_name, client_name = parse_join(join_req)
        room_id = hash(room_name) % 255
        join_id = hash(client_name) % 255

        new_client = Client(
            client_name,
            join_id,
            client_socket,
            client_address
        )

        if room_id not in CHATROOMS_MAP.keys():
            CHATROOMS_MAP[room_id] = Chatroom(room_id, room_name)

        CHATROOMS_MAP[room_id].add_client(new_client)
        client_socket.sendall(respond_to_join(
            room_name,
            room_id,
            join_id,
            client_address[1]
        ))

        return new_client


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
            client.address
        ))

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

    CHATROOMS_MAP[room_id].remove_client(client)
    client.socket.sendall(respond_to_leave(room_id, client.join_id))


def process_message_req(client, message):
    room_id, join_id, message_text = parse_message(message)
    if room_id not in CHATROOMS_MAP.keys():
        client.socket.sendall(respond_with_error(2))
        return

    elif join_id not in CHATROOMS_MAP[room_id].connected_clients.keys():
        client.socket.sendall(respond_with_error(4))
        return

    CHATROOMS_MAP[room_id].broadcast_message(
        client.join_id,
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
