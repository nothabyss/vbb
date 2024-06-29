import unittest
from vbb.datalayer.blockchain2 import Block


class TestBlockChain(unittest.TestCase):
    def test_sum_positive_numbers(self):
        result = Block.pow()
        print(result)


if __name__ == '__main__':
    unittest.main()