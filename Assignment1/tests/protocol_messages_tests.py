import unittest
import sys
sys.path.append('../src')

from protocol_messages import check_hello, check_kill, check_join, check_leave, check_message, parse_join, parse_leave


class TestValidations(unittest.TestCase):
    def test_hello(self):
        self.assertTrue(check_hello('HELO\n'))
        self.assertTrue(check_hello('HELO BASE_TEST\n'))
        self.assertTrue(check_hello('HELO BASE TEST\n'))

        self.assertFalse(check_hello('HELO BASE_TEST'))
        self.assertFalse(check_hello('HELLO\n'))
        self.assertFalse(check_hello('HELOBASE_TEST\n'))

    def test_kill(self):
        self.assertTrue(check_kill('KILL_SERVICE\n'))

        self.assertFalse(check_kill('KILL_SERVICE'))
        self.assertFalse(check_kill('KILL SERVICE\n'))
        self.assertFalse(check_kill('kill_service\n'))

    def test_join(self):
        self.assertTrue(check_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n"))

        self.assertTrue(check_join(
            "JOIN_CHATROOM: chatroom 1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client 1\n"))

        self.assertTrue(check_join(
            "JOIN_CHATROOM: chatroom 1 1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: mad max 21\n"))

        self.assertTrue(check_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: mad_max_21\n"))

        self.assertFalse(check_join(
            "JOIN_CHATROOM: \nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n"))

        self.assertFalse(check_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: \n"))

        self.assertFalse(check_join(
            "JOIN_CHATROOM:chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n"))

        self.assertFalse(check_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME:client_1\n"))

        self.assertFalse(check_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP:0\nPORT: 0\nCLIENT_NAME: client_1\n"))

        self.assertFalse(check_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT:0\nCLIENT_NAME: client_1\n"))

    def test_leave(self):
        self.assertTrue(check_leave(
            "LEAVE_CHATROOM: 123\nJOIN_ID: 456\nCLIENT_NAME: client_1\n"))

        self.assertTrue(check_leave(
            "LEAVE_CHATROOM: 123\nJOIN_ID: 456\nCLIENT_NAME: client 1\n"))

        self.assertTrue(check_leave(
            "LEAVE_CHATROOM: 123\nJOIN_ID: 456\nCLIENT_NAME: mad max 21\n"))

        self.assertTrue(check_leave(
            "LEAVE_CHATROOM: 123\nJOIN_ID: 456\nCLIENT_NAME: mad_max_21\n"))

        self.assertFalse(check_leave(
            "LEAVE_CHATROOM: room_1\nJOIN_ID: 456\nCLIENT_NAME: client_1\n"))

        self.assertFalse(check_leave(
            "LEAVE_CHATROOM: 123\nJOIN_ID: fourfivesix\nCLIENT_NAME: client_1\n"))

    def test_message(self):
        self.assertTrue(check_message(
            "CHAT: 21\nJOIN_ID: 123\nCLIENT_NAME: jack\nMESSAGE: This is a message\n\n"))

        self.assertTrue(check_message(
            "CHAT: 21\nJOIN_ID: 123\nCLIENT_NAME: jack\nMESSAGE: This is a message! Wow with punctuation?\n\n"))

        self.assertTrue(check_message(
            "CHAT: 21\nJOIN_ID: 123\nCLIENT_NAME: jack\nMESSAGE: Thisisamessagewithnospaces\n\n"))

        self.assertTrue(check_message(
            "CHAT: 21\nJOIN_ID: 123\nCLIENT_NAME: jack\nMESSAGE: This is a message\nOn multiple lines\n\n"))

        self.assertFalse(check_message(
            "CHAT: chatroom1\nJOIN_ID: 123\nCLIENT_NAME: jack\nMESSAGE: This is a message\n\n"))

        self.assertFalse(check_message(
            "CHAT: 21\nJOIN_ID: player1\nCLIENT_NAME: jack\nMESSAGE: This is a message\n\n"))

        self.assertFalse(check_message(
            "CHAT: 21\nJOIN_ID: 123\nCLIENT_NAME: \nMESSAGE: This is a message\n\n"))

        self.assertFalse(check_message(
            "CHAT: 21\nJOIN_ID: \nCLIENT_NAME: jack\nMESSAGE: This is a message\n\n"))

        self.assertFalse(check_message(
            "CHAT: 21\nJOIN_ID: 123\nCLIENT_NAME: \nMESSAGE: This is a message\n\n"))

        self.assertFalse(check_message(
            "CHAT: 21\nJOIN_ID: 123\nCLIENT_NAME: jack\nMESSAGE: This is a message\n"))

        self.assertFalse(check_message(
            "CHAT: 21\nJOIN_ID: \nCLIENT_NAME: jackMESSAGE: This is a message\n\n"))

    def test_parse_join(self):
        chatroom_name, client_name = parse_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n")
        self.assertEqual(chatroom_name, "chatroom_1")
        self.assertEqual(client_name, "client_1")

        chatroom_name, client_name = parse_join(
            "JOIN_CHATROOM: chatroom 1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client 1\n")
        self.assertEqual(chatroom_name, "chatroom 1")
        self.assertEqual(client_name, "client 1")

    def test_parse_leave(self):
        room_id, join_id = parse_leave(
            "LEAVE_CHATROOM: 543\nJOIN_ID: 211\nCLIENT_NAME: client_1\n")
        self.assertEqual(room_id, 543)
        self.assertEqual(join_id, 211)


if __name__ == '__main__':
    unittest.main()
