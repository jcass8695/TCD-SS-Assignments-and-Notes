from protocol_messages import ProtocolMessages as pr_msg


"""
Predefined responses that the server will use to respond
to the clients messages
"""

response_table = {
    # received data, server IP, server port
    pr_msg.HELLO: "HELO text\nIP:{}\nPort:{}\nStudentID:14320816\n",
    pr_msg.KILL: "Killing server, I hope you're happy\n"
}


def findResponse(message, ip="127.0.0.1", port="3000", client_name=None, join_id=None, room_ref=None):
    # If the message received was a valid ProtocolMessages enum value
    # we can look it up in the response_table
    if pr_msg.validMessage(message):
        if message == pr_msg.HELLO.value:
            return str(response_table.get(pr_msg.HELLO)).format(ip, port)

        elif message == pr_msg.KILL:
            return None

        # TODO: implement the remaining messages

    else:
        return pr_msg.ERROR.value
