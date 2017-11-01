from protocol_responses import respond_to_message


class Chatroom:
    def __init__(self, room_id, room_name):
        self.room_id = room_id
        self.room_name = room_name
        self.connected_clients = {}

    def add_client(self, new_client):
        if new_client.join_id not in self.connected_clients.keys():
            self.connected_clients[new_client.join_id] = new_client
            self.broadcast_message(new_client.join_id, new_client.handle)
            print("{} Joined chatroom {}".format(
                new_client.handle, self.room_name)
            )

    def remove_client(self, join_id):
        if join_id in self.connected_clients:
            del self.connected_clients[join_id]
            return 0
        else:
            return -1

    def get_client(self, join_id):
        return self.connected_clients.get(join_id, -1)

    def broadcast_message(self, broadcaster_join_id, broadcaster_handle):
        for join_id, client in self.connected_clients.items():
            if join_id == broadcaster_join_id:
                continue
            else:
                client.socket.sendall(respond_to_message(
                    self.room_id,
                    broadcaster_handle,
                    respond_to_message(
                        self.room_id,
                        client.handle,
                        "{} Joined".format(client.handle)
                    )
                ))
