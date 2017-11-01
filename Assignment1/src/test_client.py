import socket
import protocol_messages as pr_msg
import time


def run():
    HOST, PORT = "localhost", 3000
    data = "JOIN_CHATROOM: dragon\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: night_hawk\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    count = 1
    while True:
        try:
            # Connect to server and send data
            sock.sendall(data.encode())
            # Receive data from the server and shut down
            received = sock.recv(1024).decode()
            print(count)
            print("Sent: {}".format(data))
            print("Received: {}".format(received))
            count += 1
            time.sleep(10)

        except KeyboardInterrupt:
            sock.close()
            break


if __name__ == "__main__":
    run()
