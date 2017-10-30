import socket

import protocol_messages as pr_msg


def run():
    print("test_client running")
    HOST, PORT = "localhost", 3000
    data = "HELO BASE_SERVER\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(data.encode())

        # Receive data from the server and shut down
        received = sock.recv(1024).decode()
        print("Sent: {}".format(data))
        print("Received: {}".format(received))

        while True:
            pass

    except Exception as e:
        sock.close()


if __name__ == "__main__":
    run()
