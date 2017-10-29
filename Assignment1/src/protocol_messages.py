from re import match

"""
Predefined protocol messages that the client will send to
the server and the server can use to check if a sent message
was valid
"""
# HELLO is a special case and this constant will never be called
HELLO = "HELO\n"
KILL = "KILL_SERVICE\n"
ERROR = "INVALID_MESSAGE\n"

def check_hello(message):
    return match('HELO( \w+)*', message)

def validMessage(message):
    if check_hello(message):
        return True
