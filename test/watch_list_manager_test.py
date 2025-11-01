import os
import unittest
from datetime import datetime

from src.model.PropertyManager import PropertyManager
from src.portable.WatchListManager import WatchListManager
from src.util.PropertyFileReader import PropertyFileReader
from test_utils import TestUtils


class MyTestCase(unittest.TestCase):

    def setUp(self):
        print("Setup")
        self.property_file_reader = PropertyFileReader("resources/test-config.properties")
        self.property_file_manager = PropertyManager(self.property_file_reader)
        os.makedirs(self.property_file_manager.getStaticDirectory(), exist_ok=True)
        self.feeds_directory = self.property_file_manager.getFeedsDirectory() + "/" + datetime.now().strftime("%Y-%m-%d")
        self.temp_directory = self.property_file_manager.getTempDirectory()
        os.makedirs(self.feeds_directory,  exist_ok=True)
        os.makedirs(self.temp_directory, exist_ok=True)

    def test_sound(self):
        TestUtils.generate_test_file(self.feeds_directory, "client.txt", self.test_data())
        TestUtils.generate_test_file(self.property_file_manager.getStaticDirectory(), "watchlist.txt", self.user_entry_data())
        TestUtils.generate_test_file(self.temp_directory, "temp_userlist_" + datetime.now().strftime("%Y-%m-%d") + ".txt", self.user_entry_data())
        watch_list_manager = WatchListManager(self.property_file_manager)
        watch_list_manager.showTodaysWatchList()
        # need to add a valid assert here.

    def test_data(self) -> str:
        return ("Client1|Brazilian|Destination1|10|39|0|80|0|140|220|280|0|0|0|0|0|+447123321432|http://data.com/viewProfile.asp?"
                "userID=123456|2025-10-26 15:36:30|7544437|0|London|None|13/12/2023|1.68|10|Brown "
                "Long|Brown|True|None|[]|Latin")

    def user_entry_data(self) -> str:
        return "http://data.com/viewProfile.asp?userID=123456"

    def tearDown(self):
        print("Teardown")


if __name__ == '__main__':
    unittest.main()
