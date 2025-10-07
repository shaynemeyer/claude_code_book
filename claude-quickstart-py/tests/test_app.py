import unittest
from src.app import greet


class TestApp(unittest.TestCase):

    def test_greet_happy_path(self):
        result = greet("Alice")
        self.assertTrue(result["ok"])

    def test_greet_strips_whitespace(self):
        result = greet("Bob")
        self.assertEqual(result["message"], "Hello, Bob!")

    def test_greet_rejects_empty(self):
        with self.assertRaises(ValueError):
            greet(" ")


if __name__ == "__main__":
    unittest.main()
