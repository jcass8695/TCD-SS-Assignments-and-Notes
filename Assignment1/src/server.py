import socket
import socketserver
import threading

from protocol_responses import *
from protocol_messages import *
from client import Client

HOST, PORT = "127.0.0.1", 3000
CHATROOMS = []

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

                elif check_leave(message):

                elif check_disconnect(message):

                
                print("Server responds with:\n{}".format(response))
                self.request.sendall(response.encode())

        except BrokenPipeError:
            print("Unexpected Disconnect")
            return

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
