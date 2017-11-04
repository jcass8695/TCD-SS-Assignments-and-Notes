import socket
import protocol_messages as pr_msg
import time


def run():
    HOST, PORT = "localhost", 3000
    data = "JOIN_CHATROOM: dragon\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: night_hawk\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    try:
        # Connect to server and send data
        sock.sendall(data.encode())
        print("Sent:\n{}".format(data))

        while True:
            received = sock.recv(1024).decode()
            if received is None:
                break

            print("Received:\n{}".format(received))

    except (KeyboardInterrupt, BrokenPipeError):
        sock.close()


if __name__ == "__main__":
    run()
