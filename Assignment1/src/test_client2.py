import socket
import protocol_messages as pr_msg
import time


def run():
    HOST, PORT = "localhost", 3000
    data1 = "JOIN_CHATROOM: dragon\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: polar_bear\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    try:
        # Connect to server and send data
        sock.sendall(data1.encode())
        print("Sent:\n{}".format(data1))
        received = sock.recv(1024).decode()
        print("Received:\n{}".format(received))

        room_id = input()
        join_id = input()
        data2 = "DISCONNECT: 0\nPORT: 0\nCLIENT_NAME: polar_bear"
        time.sleep(2)
        sock.sendall(data2.encode())
        print("Sent:\n{}".format(data2))
        received = sock.recv(1024).decode()
        print("Received:\n{}".format(received))

        while True:
            pass

    except (KeyboardInterrupt, BrokenPipeError):
        pass

    sock.close()


if __name__ == "__main__":
    run()
