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

CONNECTION_LIST = []


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
    print("New thread")
    # client_socket.setblocking(True)
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode()
            if message:
                print("Server received: {}".format(message))
                if check_join(message):
                    room_name, client_handle = parse_join(message)
                    new_client = Client(
                        client_handle,
                        hash(client_handle),
                        client_socket
                    )

                    CONNECTION_LIST.append(new_client)
                    room_id = hash(room_name)
                    join_id = hash(client_handle)
                    if room_id not in CHATROOMS_MAP.keys():
                        # Create the room if it doesn't exist
                        CHATROOMS_MAP[room_id] = Chatroom(room_id, room_name)

                    CHATROOMS_MAP[room_id].add_client(new_client)
                    client_socket.sendall(respond_to_join(
                        room_name,
                        room_id,
                        join_id,
                        client_address[1]))

            else:
                raise Exception

        except Exception as e:
            print("Exception in client_thread")
            print(e)
            client_socket.close()
            break


if __name__ == "__main__":
    run()
