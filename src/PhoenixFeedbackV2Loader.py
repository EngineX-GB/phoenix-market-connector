import datetime
import json
import os
import re
import sys
import time
import requests


class PageData:

    def __init__(self, page_number, page_size, total_count, total_pages):
        self.page_number = page_number
        self.page_size = page_size
        self.total_count = total_count
        self.total_pages = total_pages

    def get_total_pages(self):
        return self.total_pages

    def get_page_number(self):
        return self.page_number

class FeedbackV2:

    def __init__(self, id, forUserId, forUserName, byUserId, byUserName, byUserTotalRating, ratingDate, isPositive,
                isNegative, isNeutral, isDisputed, feedback, feedbackResponse, ratingType, userType, userActive):
        self.id = id
        self.forUserId = forUserId
        self.forUserName = forUserName
        self.byUserId = byUserId
        self.byUserName = byUserName
        self.byUserTotalRating = byUserTotalRating
        self.ratingDate = ratingDate
        self.isPositive = isPositive
        self.isNegative = isNegative
        self.isNeutral = isNeutral
        self.isDisputed = isDisputed
        self.feedback = feedback
        self.feedbackResponse = feedbackResponse
        self.ratingType = ratingType
        self.userType = userType
        self.userActive = userActive
        self.delimiter = "|"

    def generateRecord(self):
        return "".join([str(self.id), self.delimiter,
                        str(self.forUserName), self.delimiter,
                        str(self.byUserId), self.delimiter,
                        str(self.byUserName), self.delimiter,
                        str(self.byUserTotalRating), self.delimiter,
                        str(self.ratingDate), self.delimiter,
                        str(self.isPositive), self.delimiter,
                        str(self.isNegative), self.delimiter,
                        str(self.isNeutral), self.delimiter,
                        str(self.isDisputed), self.delimiter,
                        str(self.feedback), self.delimiter,
                        str(self.feedbackResponse), self.delimiter,
                        str(self.ratingType), self.delimiter,
                        str(self.userType), self.delimiter,
                        str(self.userActive)])



"""
You can run this in 2 modes:

1. Normal mode = where you fetch one page of feedback per day.
2. Global mode = A mode that you run as a one off to get all feedback for a user. You must supply the full global list
                 of user ids and store in app-data/static/global-user-id-list.txt
                 
                 
To run in global mode:

python PhoenixFeedbackV2Loader.py --global

Ensure:
    1. the 'app.headers.json' file is present in properties folder
    2. the global-userid-list.txt file (containing all the userids) is present in the app-data/static folder

"""


class PhoenixFeedbackV2Loader:

    def __init__(self):
        pass

    """
        This code was grabbed from PhoenixFeedbackFetcher.py. Check to see if it's possible to put this function
        into a common class for reusability
    """

    def extractUserId(self, text):
        res = re.search("userID\\=([0-9]+)", text)
        return res.group(1)

    def addFeedbackEntryIntoTempFile(self, userId, isGlobal):
        if isGlobal:
            temp_file_path = ".././app-data/temp/temp_feedback-v2_global.txt"
        else:
            temp_file_path = ".././app-data/temp/temp_feedback-v2_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt"

        if not os.path.exists(temp_file_path):
            # create the file
            f = open(temp_file_path, 'w', encoding='utf-8').close()

        tempFile = open(
            temp_file_path,
            "a",
            encoding="utf-8")
        tempFile.write(userId + "\n")
        tempFile.close()

    """
    To return the list of user ids where feedback data has already been downloaded (only for feedback data today. 
    Not used for global.
    """
    def read_user_ids_from_temp_feedback_file(self, isGlobal):
        if isGlobal:
            temp_feed_file_path = ".././app-data/temp/temp_feedback-v2_global.txt"
        else:
            temp_feed_file_path = ".././app-data/temp/temp_feedback-v2_" + datetime.datetime.now().strftime(
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
     this function will go into the temp_userlist file to get the list of users (in the form of profile urls)
     for today and return them as a list
    """
    def read_profile_urls_from_userlist_temp_file(self):
        temp_userlist_feed_file_path = ".././app-data/temp/temp_userlist_" + datetime.datetime.now().strftime(
            "%Y-%m-%d") + ".txt"
        f = open(temp_userlist_feed_file_path, 'r', encoding='utf-8')
        urls = f.readlines()
        f.close()
        return urls

    """
    Locate the global userid list, read all the user ids and load feedback data
    based on the global list. This should only be done onetime only
    """
    def read_global_userid_list(self):
        global_userid_list_path = ".././app-data/static/global-userid-list.txt"
        f = open(global_userid_list_path, 'r', encoding='utf-8')
        user_id_list = f.readlines()
        f.close()
        return user_id_list

    def get_pagedata_for_feedback_loading(self, data) -> PageData:

        page_data_node = data["Result"]["pageData"]
        return PageData(page_data_node["pageNumber"],
                        page_data_node["pageSize"],
                        page_data_node["totalCount"],
                        page_data_node["totalPages"])

    def load_data(self, response_json, user_id, page_number_ref, isGlobal):
        print("[INFO] Loading feedback data for user " + user_id + ", page ref : " + str(page_number_ref))
        feedback_data = response_json["Result"]["data"]

        feedback_collection = list()
        for item in feedback_data:
            feedbackRecord = FeedbackV2(item["id"], item["forUserID"],
                                        item["forUserNickname"], item["byUserID"],
                                        item["byUserNickname"],
                                        item["byUserTotalRating"], item["ratingDate"],
                                        item["isPositive"],
                                        item["isNegative"], item["isNeutral"], item["isDisputed"],
                                        item["feedback"],
                                        item["feedbackResponse"],
                                        item["ratingType"],
                                        item["userType"], item["userActive"])
            feedback_collection.append(feedbackRecord)

        # here, try and write to persistence/ storage
        if isGlobal:
            feeds_directory = ".././app-data/feeds-feedbackv2-phoenix/global"
        else:
            feeds_directory = ".././app-data/feeds-feedbackv2-phoenix/" + datetime.datetime.now().strftime("%Y-%m-%d")

        if not os.path.exists(feeds_directory):
            os.makedirs(feeds_directory)
        feed_file_path = feeds_directory + "/" + "feeds-feedbackv2-phoenix_" + user_id + "_" + datetime.datetime.now().strftime("%Y-%m-%d") + "_" + str(page_number_ref) + ".txt"
        self.generate_feed_file(feedback_collection, feed_file_path)

    def generate_feed_file(self, records, feed_file_path):
        f = open(feed_file_path, 'w', encoding='utf-8')
        for r in records:
            f.write(r.generateRecord() + "\n")
        f.close()

    def get_json_data(self, user_id, page_number):
        url = "<VENDOR_URL>/api/Ratings/Paginated?userId=" + user_id + "&pageNumber= " + str(
            page_number) + "&pageSize=50&v=2"
        with open(".././properties/api.headers.json") as api_headers:
            headers = json.load(api_headers)
        response = requests.get(url, headers=headers)
        # response.raise_for_status()
        if response.status_code != 200:
            print("[ERROR] : " + response.text)
            return None
        # This can cause an error. Therefore handle it better
        return response.json()

    def handlePageLimit(self, total_number_of_pages):
        return total_number_of_pages

    def load(self, user_id, isGlobal):

        responseJson = self.get_json_data(user_id, 1)
        pageMetadata = self.get_pagedata_for_feedback_loading(responseJson)

        if responseJson is not None:

            if pageMetadata.total_pages == 1:
                # then get the current page of json
                self.load_data(responseJson, user_id, 1, isGlobal)
                time.sleep(5)
            elif pageMetadata.total_pages > 1:
                # then get the current page, and the loop for the others
                self.load_data(responseJson, user_id, 1, isGlobal)
                for i in range(2, self.handlePageLimit(pageMetadata.total_pages) + 1):  # have to add a + 1 to get the last page
                    time.sleep(5)
                    feed_json = self.get_json_data(user_id, i)
                    self.load_data(feed_json, user_id, i, isGlobal)
            else:
                print("[WARN] No data is available for user " + user_id)
                time.sleep(5)

            self.addFeedbackEntryIntoTempFile(user_id, isGlobal)  # TODO: check global parameter

    def get_number_of_records(self, file_path):
        f = open(file_path, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        return len(lines)

if __name__ == "__main__":
    loader = PhoenixFeedbackV2Loader()
    isGlobal = False

    if len(sys.argv) > 1 and sys.argv[1] == "--stats":
        print("[INFO] Download feedback statistics")

        userids_in_global_list = loader.get_number_of_records(".././app-data/static/global-userid-list.txt")
        userids_with_downloaded_feedback = loader.get_number_of_records(".././app-data/temp/temp_feedback-v2_global.txt")

        print("[INFO] Number of user ids in global list: " + str(userids_in_global_list))
        print("[INFO] Number of users with feedback downloaded: " + str(userids_with_downloaded_feedback))
        print("[INFO] Remaining users to download feedback for: " + str(userids_in_global_list - userids_with_downloaded_feedback))

        exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == "--global":
        isGlobal = True
        if not os.path.exists(".././app-data/static/global-userid-list.txt"):
            print("[ERROR] global-userid-list.txt cannot be found in static directory. Exiting.")
            exit(1)

    user_id_list = []
    if not isGlobal:
        feedback_user_ids = user_ids = [line.rstrip("\n") for line in loader.read_user_ids_from_temp_feedback_file(False)]

        # check if the ratings for the user have already been downloaded.
        # if so, then ignore this user and move onto the next

        user_list_urls = loader.read_profile_urls_from_userlist_temp_file()

        for url in user_list_urls:
            userId = loader.extractUserId(url)
            user_id_list.append(userId)

    else:
        feedback_user_ids = user_ids = [line.rstrip("\n") for line in loader.read_user_ids_from_temp_feedback_file(True)]
        user_id_list = [line.rstrip("\n") for line in loader.read_global_userid_list()]

    for user_id in user_id_list:
        if user_id in feedback_user_ids:
            print("[INFO] Feedback data for user : " + user_id + " is already downloaded. Ignoring...")
        else:
            loader.load(user_id, isGlobal)
