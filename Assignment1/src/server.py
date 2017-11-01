import socket
import socketserver
import threading

from protocol_responses import *
from protocol_messages import *
from client import Client
from chatroom import Chatroom

HOST = "127.0.0.1"
JOIN_PORT = 3000

# Map of join_id's to Client objects
CLIENT_PORTS_MAP = {}

# Map of room_id's to Chatroom objects
CHATROOMS_MAP = {}


def run():


if __name__ == "__main__":
    run()
