from protocol_responses import respond_to_message


class Chatroom:
    def __init__(self, room_id, room_name):
        self.room_id = room_id
        self.room_name = room_name

        # Map of join id's to Client objects
        self.connected_clients = {}

    def add_client(self, new_client):
        if new_client.join_id not in self.connected_clients.keys():
            self.connected_clients[new_client.join_id] = new_client
            self.broadcast_message(
                new_client.handle,
                "{} Joined {}".format(new_client.handle, self.room_name))

            print("{} Joined {}".format(new_client.handle, self.room_name))
            return True
        else:
            print("{} Already Joined {}".format(
                new_client.handle, self.room_name))
            return False

    def remove_client(self, client):
        if client.join_id in self.connected_clients.keys():
            del self.connected_clients[client.join_id]
            self.broadcast_message(
                client.handle,
                "{} Left {}".format(client.handle, self.room_name))

            print("{} Left {}".format(client.handle, self.room_name))

    def get_client(self, join_id):
        return self.connected_clients.get(join_id, -1)

    def broadcast_message(self, broadcaster_handle, message):
        for _, client in self.connected_clients.items():
            client.socket.sendall(respond_to_message(
                self.room_id,
                broadcaster_handle,
                message
            ))
