import unittest
import sys
sys.path.append('../src')

from protocol_messages import check_hello, check_kill, check_join, parse_join


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
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n")
        )

        self.assertTrue(check_join(
            "JOIN_CHATROOM: chatroom 1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client 1\n")
        )

        self.assertTrue(check_join(
            "JOIN_CHATROOM: chatroom 1 1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: mad max 21\n")
        )

        self.assertTrue(check_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: mad_max_21\n")
        )

        self.assertFalse(check_join(
            "JOIN_CHATROOM: \nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n")
        )

        self.assertFalse(check_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: \n")
        )

        self.assertFalse(check_join(
            "JOIN_CHATROOM:chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n")
        )

        self.assertFalse(check_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME:client_1\n")
        )

        self.assertFalse(check_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP:0\nPORT: 0\nCLIENT_NAME: client_1\n")
        )

        self.assertFalse(check_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT:0\nCLIENT_NAME: client_1\n")
        )

    def test_parse_join(self):
        chatroom_name, client_ip, client_name = parse_join(
            "JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n")
        self.assertEqual(chatroom_name, "chatroom_1")
        self.assertEqual(client_ip, "0")
        self.assertEqual(client_name, "client_1")

        chatroom_name, client_ip, client_name = parse_join(
            "JOIN_CHATROOM: chatroom 1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client 1\n")
        self.assertEqual(chatroom_name, "chatroom 1")
        self.assertEqual(client_ip, "0")
        self.assertEqual(client_name, "client 1")


if __name__ == '__main__':
    unittest.main()
