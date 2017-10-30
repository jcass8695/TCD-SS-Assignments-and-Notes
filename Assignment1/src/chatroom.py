class Chatroom:
    def __init__(self, room_id, room_name):
        self.room_id = room_id
        self.room_name = room_name
        self.connected_clients = {}

    def add_client(self, join_id, new_client):
        if join_id not in self.connected_clients.keys():
            self.connected_clients[join_id] = new_client
            return 0
        else:
            return -1

    def remove_client(self, join_id):
        if join_id in self.connected_clients.keys():
            del self.connected_clients[join_id]
            return 0
        else:
            return -1


    def get_client(self, join_id):
        return self.connected_clients.get(join_id, None)

    def broadcast_message(self, broadcaster_join_id, message):
        for join_id, client in self.connected_clients:
            if join_id == broadcaster_join_id:
                continue
            else:
                client.socket.sendall(message)
