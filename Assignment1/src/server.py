import socketserver
import threading

import protocol_responses as pr_resp
from protocol_messages import ProtocolMessages as pr_msg

HOST, PORT = "127.0.0.1", 3000


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The Request Handler class for our server

    It is instantiated once per connection to the server, and must
    override the handle() method to communicate with the client.

    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).decode()
        print("{} wrote: ".format(self.client_address[0]))
        print(self.data)

        response = pr_resp.findResponse(self.data)

        if response is None:
            self.server.shutdown()
            return
        print("Server responds with:\n{}".format(response))

        self.request.sendall(response.encode())


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
