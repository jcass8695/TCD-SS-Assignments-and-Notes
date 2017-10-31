import socket
import socketserver
import threading

from protocol_responses import *
from protocol_messages import *
from client import Client
from chatroom import Chatroom

HOST = "127.0.0.1"
JOIN_PORT = 3000

# Map of join_id's to Client objects
CLIENT_PORTS_MAP = {}

# Map of room_id's to Chatroom objects
CHATROOMS_MAP = {}


class JoinServerTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            message = self.request.recv(1024).decode()
            print('Server received: {}'.format(message))
            if check_hello(message):
                response = respond_to_hello(message)

            elif check_kill(message):
                self.server.shutdown()
                return

            elif check_join(message):
                response = self.handle_join(message)

            print("Server responds with:\n{}".format(response))
            self.request.sendall(response.encode())

        except BrokenPipeError:
            print("Unexpected Disconnect")
            return

    def handle_join(self, message):
        chatroom_name, client_ip, client_name = parse_join(message)
        room_id = hash(chatroom_name)
        join_id = hash(client_name)

        # Check if client already exists, so we don't reassign ports
        if join_id not in CLIENT_PORTS_MAP:
            new_client = Client(
                client_name,
                join_id,
                socketserver.ThreadingTCPServer(
                    (HOST, 0),
                    MessageTCPHandler
                )
            )

            CLIENT_PORTS_MAP[join_id] = new_client

        else:
            new_client = CLIENT_PORTS_MAP[join_id]

        # Check if chatroom exists, if not create it
        if room_id not in CHATROOMS_MAP:
            CHATROOMS_MAP[room_id] = Chatroom(
                room_id,
                chatroom_name
            )

        # Check if client is already in chatroom
        if CHATROOMS_MAP[room_id].add_client(new_client) == -1:
            return respond_with_error()

        else:
            # Tell the client to now connect over the given port
            return respond_to_join(
                chatroom_name,
                room_id,
                join_id,
                new_client.port
            )


class MessageTCPHandler(JoinServerTCPHandler):
    def handle(self):
        return


def run():
    try:
        print("Server running")

        # Prevent TCP TIME_WAIT
        socketserver.ThreadingTCPServer.allow_reuse_address = True
        server = socketserver.ThreadingTCPServer(
            (HOST, JOIN_PORT),
            JoinServerTCPHandler
        ).serve_forever()

    except KeyboardInterrupt:
        pass

    print("\nClosing server")
    server.server_close()


if __name__ == "__main__":
    run()
