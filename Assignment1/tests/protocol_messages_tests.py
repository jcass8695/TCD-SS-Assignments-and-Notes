import unittest
import sys
sys.path.append('../src')

from protocol_messages import check_hello, check_kill, check_join

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
        self.assertTrue(check_join("JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n"))
        self.assertTrue(check_join("JOIN_CHATROOM: chatroom 1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client 1\n"))
        self.assertTrue(check_join("JOIN_CHATROOM: chatroom 1 1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: mad max 21\n"))
        self.assertTrue(check_join("JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: mad_max_21\n"))

        self.assertFalse(check_join("JOIN_CHATROOM: \nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n"))
        self.assertFalse(check_join("JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: \n"))
        self.assertFalse(check_join("JOIN_CHATROOM:chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: client_1\n"))
        self.assertFalse(check_join("JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME:client_1\n"))
        self.assertFalse(check_join("JOIN_CHATROOM: chatroom_1\nCLIENT_IP:0\nPORT: 0\nCLIENT_NAME: client_1\n"))
        self.assertFalse(check_join("JOIN_CHATROOM: chatroom_1\nCLIENT_IP: 0\nPORT:0\nCLIENT_NAME: client_1\n"))






if __name__ == '__main__':
    unittest.main()
