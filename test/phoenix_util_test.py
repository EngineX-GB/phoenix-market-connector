import unittest

from src.util.PhoenixUtil import PhoenixUtil


class PhoenixUtilTest(unittest.TestCase):

    def test_something(self):
        res = 1 > 0
        self.assertTrue(res)

    def test_today_date(self):
        today_date = PhoenixUtil.getTodaysDate()
        self.assertIsNotNone(today_date)

    def test_convert_height(self):
        height = PhoenixUtil.convertHeight("5'7\"")
        self.assertEqual("1.70", height)

    def test_extract_userId(self):
        string_containing_userId = "userID=12345678"
        userId = PhoenixUtil.extractUserId(string_containing_userId)
        self.assertEqual("12345678", userId)

    if __name__ == "__main__":
        unittest.main()
