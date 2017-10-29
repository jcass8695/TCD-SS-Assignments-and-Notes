import unittest
import sys
sys.path.append('../src')

from protocol_messages import check_hello

class TestValidations(unittest.TestCase):
    def test_helo(self):
        self.assertTrue(check_hello('HELO'))
        self.assertTrue(check_hello('HELO BASE_TEST'))
        self.assertTrue(check_hello('HELO BASE TEST'))
        self.assertFalse(check_hello('HELLO'))
        self.assertTrue(check_hello('HELOBASE_TEST'))


if __name__ == '__main__':
    unittest.main()
