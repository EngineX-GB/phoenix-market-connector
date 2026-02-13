import datetime
import os
import re
from abc import ABC

from util.PhoenixIOUtil import PhoenixIOUtil


class PhoenixAbstractV2DataLoader(ABC):

    def __init__(self):
        pass

    def get_number_of_records(self, file_path):
        f = open(file_path, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        return len(lines)


    def extractUserId(self, text):
        res = re.search("userID\\=([0-9]+)", text)
        return res.group(1)


    def read_global_userid_list(self):
        global_userid_list_path = ".././app-data/static/global-userid-list.txt"
        f = open(global_userid_list_path, 'r', encoding='utf-8')
        user_id_list = f.readlines()
        f.close()
        return user_id_list

    def read_profile_urls_from_userlist_temp_file(self):
        temp_userlist_feed_file_path = ".././app-data/temp/temp_userlist_" + datetime.datetime.now().strftime(
            "%Y-%m-%d") + ".txt"
        f = open(temp_userlist_feed_file_path, 'r', encoding='utf-8')
        urls = f.readlines()
        f.close()
        return urls

    # TODO: get profile URLs of user data that have more than zero feedback. (Saves time downloading data)
    def read_profile_urls_from_userlist_temp_file_with_more_than_zero_feedback(self):
        # it will go into todays feed data and capture all the lines. Then check the rating value.
        # if the rating is 0, then ignore the line. Only get the feedback data for the client if
        # they have a non-zero feedback

        all_feed_lines = PhoenixIOUtil.fetch_all_feed_data(".././app-data/feeds")
        print(f"[INFO] Number of clients captured in all the feed files : {len(all_feed_lines)}")
        profile_urls = list()
        for line in all_feed_lines:
            fields = line.split("|")
            if fields[3] != "0":
                profile_urls.append(fields[17])
        print(f"[INFO] Number of clients with non-zero feedback = {len(profile_urls)}")
        print(f"[INFO] Number of clients with zero feedback = {len(all_feed_lines) - len(profile_urls)}")
        print(f"[INFO] % of clients with non-zero feedback = {(len(profile_urls) / len(all_feed_lines)) * 100}")
        return profile_urls

    def read_user_ids_from_temp_feedback_file(self, feedType, isGlobal):
        if isGlobal:
            temp_feed_file_path = ".././app-data/temp/temp_" + feedType + "-v2_global.txt"
        else:
            temp_feed_file_path = ".././app-data/temp/temp_" + feedType + "-v2_" + datetime.datetime.now().strftime(
                "%Y-%m-%d") + ".txt"
        if not os.path.exists(temp_feed_file_path):
            # create the file
            f = open(temp_feed_file_path, 'w', encoding='utf-8').close()
            return list()
        else:
            temp_file = open(temp_feed_file_path, "r", encoding="utf-8")
            user_ids = temp_file.readlines()
            temp_file.close()
        return user_ids


    """
        feedType is either 'servicereports' or 'feedback' depending on the type of
        feed being loaded.
    """
    def update_temp_file(self, user_id, isGlobal, feedType):
        if isGlobal:
            temp_file_path = ".././app-data/temp/temp_" + feedType+ "-v2_global.txt"
        else:
            temp_file_path = ".././app-data/temp/temp_" + feedType + "-v2_" + datetime.datetime.now().strftime(
                "%Y-%m-%d") + ".txt"
        if not os.path.exists(temp_file_path):
            f = open(temp_file_path, 'w', encoding="utf-8")
            f.write(user_id + "\n")
            f.close()
        else:
            f = open(temp_file_path, 'a', encoding="utf-8")
            f.write(str(user_id) + "\n")
            f.close()
