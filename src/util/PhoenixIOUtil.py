import datetime
import os

class PhoenixIOUtil:

    @staticmethod
    def update_data_file(filepath, write_mode, lines: list[str]):
        f = open(filepath, write_mode, encoding='utf-8')
        for line in lines:
            f.write(line + "\n")
        f.close()

    @staticmethod
    def create_blank_file(filepath: str):
        open(filepath, 'w', encoding='utf-8').close()

    @staticmethod
    def fetch_all_feed_data(feedsDirectory: str):
        todaysFeedDirectory = feedsDirectory + "/" + datetime.datetime.now().strftime("%Y-%m-%d")
        all_lines = list()
        if os.path.exists(todaysFeedDirectory):
            # loop through each file
            feed_files = os.listdir(todaysFeedDirectory)
            for feed in feed_files:
                if os.path.isfile(todaysFeedDirectory + "/" + feed):
                    # open the file, get the lines and save them in a big list.
                    f = open(todaysFeedDirectory + "/" + feed, 'r', encoding='utf-8')
                    lines = f.readlines()
                    all_lines.extend(lines)
                    f.close()
        else:
            print(f"[ERROR] {todaysFeedDirectory} does not exist.")
        return all_lines

    @staticmethod
    def get_os_name():
        if os.name == "nt":
            return "Windows"
        else:
            return os.name
