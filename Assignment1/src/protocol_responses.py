from time import time
from datetime import datetime
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
    pr_msg.MESSAGE: "CHAT: {}\nCLIENT_NAME: {}\nMESSAGE: {}\n\n",
    pr_msg.ERROR1: "Invalid Join Request",
    pr_msg.ERROR2: "Invalid Request: Chatroom doesn't exist",
    pr_msg.ERROR3: "Invalid Request: Join ID's don't match",
    pr_msg.ERROR4: "Invalid Request: User is not in this chatroom",
    pr_msg.ERROR5: "invalid Request: Client handles dont match"
}


def respond_to_hello(message, ip, port="3000"):
    # Check if there's extra text beside the 'HELO'
    if len(message.split(' ', maxsplit=1)) > 1:
        extra_text = ' ' + message.split(' ', maxsplit=1)[1].strip()
        response = str(RESPONSE_TABLE.get(pr_msg.HELLO)).format(extra_text, ip, port).encode()
    else:
        response = str(RESPONSE_TABLE.get(pr_msg.HELLO)).format('', ip, port).encode()

    print("{}\n{}".format(datetime.utcfromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S"), response.decode()))
    return response


def respond_to_join(chatroom_name, room_id, join_id, ip, port):
    response = str(RESPONSE_TABLE.get(pr_msg.JOIN)).format(chatroom_name, ip, port, room_id, join_id).encode()
    print("{}\n{}".format(datetime.utcfromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S"), response.decode()))
    return response

def respond_to_leave(room_id, join_id):
    response = str(RESPONSE_TABLE.get(pr_msg.LEAVE)).format(room_id, join_id).encode()
    print("{}\n{}".format(datetime.utcfromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S"), response.decode()))
    return response

def respond_to_message(room_id, client_name, message):
    response = str(RESPONSE_TABLE.get(pr_msg.MESSAGE)).format(room_id, client_name, message).encode()
    print("{}\n{}".format(datetime.utcfromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S"), response.decode()))
    return response

def respond_with_error(error_id):
    response = ''
    if error_id is 1:
        response = str(RESPONSE_TABLE.get(pr_msg.ERROR1)).encode()

    elif error_id is 2:
        response = str(RESPONSE_TABLE.get(pr_msg.ERROR2)).encode()

    elif error_id is 3:
        response = str(RESPONSE_TABLE.get(pr_msg.ERROR2)).encode()

    elif error_id is 4:
        response = str(RESPONSE_TABLE.get(pr_msg.ERROR2)).encode()

    elif error_id is 5:
        response = str(RESPONSE_TABLE.get(pr_msg.ERROR2)).encode()

    else:
        response = "Invalid request, Error".encode()

    print("{}\n{}".format(datetime.utcfromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S"), response.decode()))
    return response
