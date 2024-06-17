import unittest
from blockchain2 import Blockchain, Block


class TestBlockChain(unittest.TestCase):
    def test_sum_positive_numbers(self):
        result = Block.pow()
        print(result)


if __name__ == '__main__':
    unittest.main()