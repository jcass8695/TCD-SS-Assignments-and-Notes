import unittest
import sys
sys.path.append('../src')

from protocol_messages import check_hello, check_kill

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

if __name__ == '__main__':
    unittest.main()
