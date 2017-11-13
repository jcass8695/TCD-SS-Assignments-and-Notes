from threading import Lock
from protocol_responses import respond_to_message

class Chatroom:
    def __init__(self, room_id, room_name):
        self.room_id = room_id
        self.room_name = room_name

        # Map of join id's to Client objects
        self.connected_clients = {}
        self.mutex = Lock()

    def add_client(self, new_client):
        try:
            self.mutex.acquire()
            if new_client.join_id not in self.connected_clients.keys():
                self.connected_clients[new_client.join_id] = new_client
                print("{} Joined {}".format(new_client.handle, self.room_name))
                return True
            else:
                print("{} Already Joined {}".format(
                    new_client.handle, self.room_name))
                return False
        finally:
            self.mutex.release()

    def remove_client(self, client):
        try:
            self.mutex.acquire()    
            if client.join_id in self.connected_clients.keys():
                del self.connected_clients[client.join_id]
                print("{} Left {}".format(client.handle, self.room_name))
        finally:
            self.mutex.release()

    def broadcast_message(self, broadcaster_handle, message):
        try:
            self.mutex.acquire()
            for _, client in self.connected_clients.items():
                print("> {}".format(client.handle))
                client.socket.sendall(respond_to_message(
                    self.room_id,
                    broadcaster_handle,
                    message
                ))
        finally:
            self.mutex.release()
