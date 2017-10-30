from re import match

"""
Predefined protocol messages that the client will send to
the server and the server can use to check if a sent message
was valid
"""
HELLO = "HELO( \w+)*\n"
KILL = "KILL_SERVICE\n"
ERROR = "INVALID_MESSAGE\n"
JOIN = "JOIN_CHATROOM: (\w+)\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: (\w+)\n"
LEAVE = "LEAVE_CHATROOM: (\w+)\nJOIN_ID: (\w+)\nCLIENT_NAME: (\w+)\n"
DISCONNECT = "DISCONNECT: 0\nPORT: 0\nCLIENT_NAME: (\w+)\n"
MESSAGE = "CHAT: (\d+)\nJOIN_ID: (\w+)\nCLIENT_NAME: (\w+)\nMESSAGE: (\w+ )*\n\n"

def check_hello(message):
    return match(HELLO, message)

def check_kill(message):
    return match(KILL, message)

def check_join(message):
    return match(JOIN, message)

def check_leave(message):
    return match(LEAVE, message)

def check_disconnect(message):
    return match(DISCONNECT, message)

def validMessage(message):
    if check_hello(message) or check_kill(message):
        return True
