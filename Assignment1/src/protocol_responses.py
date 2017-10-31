import protocol_messages as pr_msg
"""
Predefined responses that the server will use to respond
to the clients messages
"""

RESPONSE_TABLE = {
    # received data, server IP, server port
    pr_msg.HELLO: "HELO{}\nIP:{}\nPort:{}\nStudentID:14320816\n",
    pr_msg.JOIN: "JOINED_CHATROOM: {}\nSERVER_IP: {}\nPORT: {}\nROOM_REF: {}\nJOIN_ID: {}\n",
    pr_msg.LEAVE: "LEFT_CHATROOM: {}\nJOIN_ID: {}\n",
    pr_msg.MESSAGE: "CHAT: {}\nCLIENT_NAME: {}\nMESSAGE: {}\n\n"
}


def respond_to_hello(message, ip="127.0.0.1", port="3000"):
    # Check if there's extra text beside the 'HELO'
    if len(message.split(' ', maxsplit=1)) > 1:
        extra_text = ' ' + message.split(' ', maxsplit=1)[1].strip()
        return str(RESPONSE_TABLE.get(pr_msg.HELLO)).format(extra_text, ip, port)
    else:
        return str(RESPONSE_TABLE.get(pr_msg.HELLO)).format('', ip, port)


def respond_to_join(chatroom_name, room_id, join_id, port, ip="127.0.0.1"):
    return str(RESPONSE_TABLE.get(pr_msg.JOIN)).format(chatroom_name, ip, port, room_id, join_id)


def respond_to_leave(room_id, join_id):
    return str(RESPONSE_TABLE.get(pr_msg.LEAVE)).format(room_id, join_id)


def respond_to_message(room_id, client_name, message):
    return str(RESPONSE_TABLE.get(pr_msg.MESSAGE)).format(room_id, client_name, message)


def respond_with_error():
    return str(RESPONSE_TABLE.get(pr_msg.ERROR))
