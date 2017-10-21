from enum import Enum


class ProtocolMessages(Enum):
    """
    Predefined protocol messages that the client will send to
    the server and the server can use to check if a sent message
    was valid
    """

    HELLO = "HELO text\n"
    KILL = "KILL_SERVICE\n"
    ERROR = "INVALID_MESSAGE\n"

    @staticmethod
    def validMessage(message):
        for valid_message in ProtocolMessages.__members__.values():
            if message == valid_message.value:
                return True

        return False
