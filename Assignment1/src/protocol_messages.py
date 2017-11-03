from re import match

"""
Predefined protocol messages that the client will send to
the server and the server can use to check if a sent message
was valid
"""
HELLO = "HELO( \w+)*\n"
KILL = "KILL_SERVICE\n"
ERROR = "INVALID_MESSAGE\n"
JOIN = "JOIN_CHATROOM: (\w+\s*)+\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: (\w+\s*)+\n"
LEAVE = "LEAVE_CHATROOM: \d+\nJOIN_ID: \d+\nCLIENT_NAME: (\w+)\n"
DISCONNECT = "DISCONNECT: 0\nPORT: 0\nCLIENT_NAME: (\w+\s*)+\n"
MESSAGE = "CHAT: \d+\nJOIN_ID: \d+\nCLIENT_NAME: (\w+\s*)+\nMESSAGE: (\w+(!|\.|\?)*\s*)+\n\n"


def check_hello(message):
    return True if match(HELLO, message) is not None else False


def check_kill(message):
    return True if match(KILL, message) is not None else False


def check_join(message):
    return True if match(JOIN, message) is not None else False


def check_leave(message):
    return True if match(LEAVE, message) is not None else False


def check_disconnect(message):
    return True if match(DISCONNECT, message) is not None else False


def check_message(message):
    return True if match(MESSAGE, message) is not None else False


def parse_join(message):
    split_message = message.split('\n')
    chatroom_name = split_message[0].split(':')[1].strip()
    client_name = split_message[3].split(':')[1].strip()
    return chatroom_name, client_name


def parse_leave(message):
    split_message = message.split('\n')
    room_id = int(split_message[0].split(':')[1].strip())
    join_id = int(split_message[1].split(':')[1].strip())
    return room_id, join_id
