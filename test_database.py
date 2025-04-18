
import unittest
from database import has_already_searched, connect

class TestDatabase(unittest.TestCase):
    def test_has_already_searched_false(self):
        self.assertFalse(has_already_searched("1900-01-01"))
        self.assertFalse(has_already_searched("1880-01-15"))
        self.assertFalse(has_already_searched("1901-02-28"))
        self.assertFalse(has_already_searched("1923-01-04"))
        self.assertFalse(has_already_searched("1955-03-10"))
        self.assertFalse(has_already_searched("1800-02-01"))
        self.assertFalse(has_already_searched("1912-01-02"))
        self.assertFalse(has_already_searched("1939-03-03"))
        self.assertFalse(has_already_searched("1899-01-19"))
        self.assertFalse(has_already_searched("1947-02-14"))
        self.assertFalse(has_already_searched("1799-03-09"))

if __name__ == "__main__":
    unittest.main()
