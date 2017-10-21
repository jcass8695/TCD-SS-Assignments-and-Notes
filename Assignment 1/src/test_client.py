import socket


def run():
    print("test_client running")
    HOST, PORT = "localhost", 3000
    data = "Hello World"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")
    finally:
        sock.close()

    print("Sent:     {}".format(data))
    print("Received: {}".format(received))
    sock.close()


run()
