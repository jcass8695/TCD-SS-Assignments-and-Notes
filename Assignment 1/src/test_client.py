import socket

from protocol_messages import ProtocolMessages


def run():
    print("test_client running")
    HOST, PORT = "localhost", 3000
    data = ProtocolMessages.KILL.value

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(data.encode())

        # Receive data from the server and shut down
        received = sock.recv(1024).decode()
        print("Sent: {}".format(data))
        print("Received: {}".format(received))

    except Exception as e:
        print(e.with_traceback())
        sock.close()


if __name__ == "__main__":
    run()
