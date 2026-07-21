import datetime
import json
import os
import time
import requests

from model.FeedbackV2 import FeedbackV2
from model.PageData import PageData
from PhoenixAbstractV2DataLoader import PhoenixAbstractV2DataLoader
from model import PropertyManager
from src.model.FeedbackV2PayloadRequest import FeedbackV2PayloadRequest
from src.service.ClientService import ClientService

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


class PhoenixFeedbackV2Loader(PhoenixAbstractV2DataLoader):

    def __init__(self, propertyManager: PropertyManager, isServiceMode: bool):
        super().__init__()
        self.propertyManager = propertyManager
        self.isServiceMode = isServiceMode

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

        if self.isServiceMode:
            # here, take the feedback_collection and put it into a rest call for the data ingestion service
            print("[DEBUG] Publishing feedback data to the data ingestion service")
            self.save_and_publish(feedback_collection, user_id)
        else:
            # here, try and write to persistence/ storage
            if isGlobal:
                feeds_directory = self.propertyManager.getFeedsFeedbackV2Directory() + "/global"
            else:
                feeds_directory = self.propertyManager.getFeedsFeedbackV2Directory() + "/" + datetime.datetime.now().strftime("%Y-%m-%d")

            if not os.path.exists(feeds_directory):
                os.makedirs(feeds_directory)
            feed_file_path = feeds_directory + "/" + "feeds-feedbackv2-phoenix_" + user_id + "_" + datetime.datetime.now().strftime(
                "%Y-%m-%d") + "_" + str(page_number_ref) + ".txt"
            self.generate_feed_file(feedback_collection, feed_file_path)



    def generate_feed_file(self, records, feed_file_path):
        f = open(feed_file_path, 'w', encoding='utf-8')
        for r in records:
            f.write(r.generateRecord() + "\n")
        f.close()

    def get_json_data(self, user_id, page_number):
        url = self.propertyManager.getApiProviderUrl() + "/api/Ratings/Paginated?userId=" + user_id + "&pageNumber= " + str(
            page_number) + "&pageSize=50&v=2"
        with open(self.propertyManager.getApiHeadersJsonPath()) as api_headers:
            headers = json.load(api_headers)
        response = requests.get(url, headers=headers)
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
                time.sleep(1)
            elif pageMetadata.total_pages > 1:
                # then get the current page, and the loop for the others
                self.load_data(responseJson, user_id, 1, isGlobal)

                # 25-01-26: Only if 'isGlobal' is true, then get all the pages of JSON data for the user.
                # otherwise if isGlobal is false (i.e. it's a standard daily feed, then just get the one page
                if isGlobal:
                    for i in range(2, self.handlePageLimit(
                            pageMetadata.total_pages) + 1):  # have to add a + 1 to get the last page
                        time.sleep(1)
                        feed_json = self.get_json_data(user_id, i)
                        self.load_data(feed_json, user_id, i, isGlobal)
            else:
                print("[WARN] No data is available for user " + user_id)
                time.sleep(1)

            self.update_temp_file(user_id, isGlobal, "feedback")

    def execute(self, args: list[str]):
        isGlobal = False

        if len(args) == 1 and args[0] == "--stats":
            print("[INFO] Download feedback statistics")

            userids_in_global_list = self.get_number_of_records(self.propertyManager.getStaticDirectory() + "/global-userid-list.txt")
            userids_with_downloaded_feedback = self.get_number_of_records(
                self.propertyManager.getTempDirectory() + "/temp_feedback-v2_global.txt")

            print("[INFO] Number of user ids in global list: " + str(userids_in_global_list))
            print("[INFO] Number of users with feedback downloaded: " + str(userids_with_downloaded_feedback))
            print("[INFO] Remaining users to download feedback for: " + str(
                userids_in_global_list - userids_with_downloaded_feedback))

            exit(0)

        if len(args) == 1 and args[0] == "--global":
            isGlobal = True
            if not os.path.exists(self.propertyManager.getStaticDirectory() + "/global-userid-list.txt"):
                print("[ERROR] global-userid-list.txt cannot be found in static directory. Exiting.")
                exit(1)

        user_id_list = []
        if not isGlobal:
            feedback_user_ids = user_ids = [line.rstrip("\n") for line in
                                            self.read_user_ids_from_temp_feedback_file("feedback", False)]

            # check if the ratings for the user have already been downloaded.
            # if so, then ignore this user and move onto the next

            # 2026-02-13: Here, check the arg list for a setting called --smartload.
            # if --smartload is set, then only get profiles with ratings greater than 0.
            # otherwise, get the whole lot, as normal.
            if "--smartloading" in args:
                print("[INFO] Smart loading is on. Clients with ratings greater than 0 will be downloaded")
                user_list_urls = self.read_profile_urls_from_userlist_temp_file_with_more_than_zero_feedback()
            else:
                print("[INFO] Smart loading is off. All client feedback will be downloaded")
                user_list_urls = self.read_profile_urls_from_userlist_temp_file()

            for url in user_list_urls:
                userId = self.extractUserId(url)
                user_id_list.append(userId)

        else:
            feedback_user_ids = user_ids = [line.rstrip("\n") for line in
                                            self.read_user_ids_from_temp_feedback_file("feedback", True)]
            user_id_list = [line.rstrip("\n") for line in self.read_global_userid_list()]

        for user_id in user_id_list:
            if user_id in feedback_user_ids:
                print("[INFO] Feedback data for user : " + user_id + " is already downloaded. Ignoring...")
            else:
                self.load(user_id, isGlobal)

    # 200726: This function is created for allowing the user to download feedback
    # for a selection of users.
    # This is not used for the portable version of the market connector, only for the service mode
    def load_by_userId (self, userIds: list[str]):
        print("[INFO] Running load function for fetching feedback-v2 in service mode")
        if self.isServiceMode:
            ClientService.send_notification("update", "load", "OK", "Loading feedback for assets started")
        for userId in userIds:
            self.load(userId, False)
        if self.isServiceMode:
            ClientService.send_notification("update", "load", "OK", "Loading feedback for assets completed")


    # TODO: Consider putting this in a persistence class for feedbackv2
    def save_and_publish(self, records: list[FeedbackV2], user_id : str):
        strRecords = []
        # the list of records will be of type PhoenixClient.
        # Convert to string before transferring over the wire.
        for r in records:
            strRecords.append(r.generateRecord())

        requestPayload = FeedbackV2PayloadRequest(records=strRecords, user_id=user_id)

        jsonRecords = json.dumps(requestPayload.model_dump())
        ingestionServiceEndpoint = self.propertyManager.getIngestionServiceEndpoint()
        response = requests.post(url=ingestionServiceEndpoint + "/feedbackv2", data=jsonRecords)
        if response.status_code != 201 and response.status_code != 200:
            print("[ERROR] Failed to publish records for ingestion. Error code : " + str(response.status_code))
        else:
            print("[INFO] Successfully published records for ingestion. Code : " + str(response.status_code))

#
# if __name__ == "__main__":
#     loader = PhoenixFeedbackV2Loader()
#     loader.execute([])
