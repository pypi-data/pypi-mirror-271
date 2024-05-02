import unittest

from velosaurus_sum.calculator import sum


class TestCalculator(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum(2, 3), 5)
        self.assertEqual(sum(-1, 1), 0)
        self.assertEqual(sum(0, 0), 0)
        self.assertEqual(sum(10, -5), 5)


if __name__ == "__main__":
    unittest.main()
