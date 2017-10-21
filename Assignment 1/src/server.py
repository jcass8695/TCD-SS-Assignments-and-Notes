import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The Request Handler class for our server

    It is instantiated once per connection to the server, and must
    override the handle() method to communicate with the client.

    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote: ".format(self.client_address))
        print(self.data)
        self.request.sendall(self.data.upper())


def run():
    try:
        print("Anton running")
        HOST, PORT = "localhost", 3000
        socketserver.TCPServer.allow_reuse_address = True
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        server.serve_forever()

    except KeyboardInterrupt:
        server.server_close()


run()
