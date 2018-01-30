import socket
import sys
import time


def run():
    HOST, PORT = sys.argv[1], 3000
    data = "JOIN_CHATROOM: chat_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n"
    data2 = "JOIN_CHATROOM: chat_2\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n"
    data3 = "JOIN_CHATROOM: chat_3\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n"
    data4 = "DISCONNECT: 0\nPORT: 0\nCLIENT_NAME: client_1\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    try:
        # Connect to server and send data
        sock.sendall(data.encode())
        print("Sent:\n{}".format(data))

        # Receive join receipt
        received = sock.recv(1024).decode()
        print("Received:\n{}".format(received))
        time.sleep(1)
        # Connect to server and send data
        sock.sendall(data2.encode())
        print("Sent:\n{}".format(data2))

        # Receive join receipt
        received = sock.recv(1024).decode()
        print("Received:\n{}".format(received))
        time.sleep(1)

        # Connect to server and send data
        sock.sendall(data3.encode())
        print("Sent:\n{}".format(data3))

        # Receive join receipt
        received = sock.recv(1024).decode()
        print("Received:\n{}".format(received))
        time.sleep(1)

        # Connect to server and send data
        sock.sendall(data4.encode())
        print("Sent:\n{}".format(data))

        while received:
            received = sock.recv(1024).decode()
            print("Received:\n{}".format(received))
            time.sleep(1)

        while True:
            pass
    except (KeyboardInterrupt, BrokenPipeError):
        sock.close()


if __name__ == "__main__":
    run()
