import socket
import socketserver
import threading

from protocol_responses import *
from protocol_messages import *
from client import Client
from chatroom import Chatroom

HOST, PORT = "127.0.0.1", 3000
CHATROOMS = {}

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The Request Handler class for our server

    It is instantiated once per connection to the server, and must
    override the handle() method to communicate with the client.
    """
    client = None

    def handle(self):
        try:
            while True:
                # self.request is the TCP socket connected to the client
                message = self.request.recv(1024).decode()
                if check_hello(message):
                    response = respond_to_hello(message)

                elif check_kill(message):
                    self.server.shutdown()
                    return

                elif check_join(message):
                    self.handle_join(message)

                elif check_leave(message):
                
                elif check_disconnect(message):               
                
                
                print("Server responds with:\n{}".format(response))
                self.request.sendall(response.encode())

        except BrokenPipeError:
            print("Unexpected Disconnect")
            return
    
    def handle_join(self, message):
        # Check if client is null 
        # Check if chatroom exists and if not create it
        # Is user already in this chatroom
        # Assign join id to client (number of people in chatroom?)
        # Add client to chatroom
        # Message chatroom telling them client_name joined
        chatroom_name, client_ip, client_name = parse_join(message)
        room_id = hash(chatroom_name)
        if client is None:
            client = Client(client_name, hash(client_name), client_ip, self.request)

        if room_id not in CHATROOMS.keys():
            CHATROOMS[room_id] = Chatroom(room_id, chatroom_name)

        if CHATROOMS[room_id].add_client(client) == -1:
            print('{} already in {}'.format(client.handle, chatroom_name))

        CHATROOMS[room_id].broadcast_message(client.join_id, client.handle, "{} joined!\n".format(client.handle))

def run():
    try:
        print("Server running")

        # Prevent TCP TIME_WAIT
        socketserver.ThreadingTCPServer.allow_reuse_address = True
        server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
        server.serve_forever()

    except KeyboardInterrupt:
        pass

    print("\nClosing server")
    server.server_close()


if __name__ == "__main__":
    run()
