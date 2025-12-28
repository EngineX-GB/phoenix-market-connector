import datetime
import json
import os
import re
import sys
import time

import requests


class ServiceReportFeed:

    def __init__(self, candidate_description, candidate_description_score, client_nickname, comments, comments_score,
                 create_date, exclude_affiliate, fee, id, location, meet_date, meet_duration, nickname, oncall,
                 personality, personality_score, rating_total, recommend, rejected, report_rating, schema_id,
                 schema_last_updated, score, services, services_score, user_id, venue_description, venue_score, vfm,
                 visit_again):
        self.candidate_description = candidate_description
        self.candidate_description_score = candidate_description_score
        self.client_nickname = client_nickname
        self.comments = comments
        self.comments_score = comments_score
        self.create_date = create_date
        self.exclude_affiliate = exclude_affiliate
        self.fee = fee
        self.id = id
        self.location = location
        self.meet_date = meet_date
        self.meet_duration = meet_duration
        self.nickname = nickname
        self.oncall = oncall
        self.personality = personality
        self.personality_score = personality_score
        self.rating_total = rating_total
        self.recommend = recommend
        self.rejected = rejected
        self.report_rating = report_rating
        self.schema_id = schema_id
        self.schema_last_updated = schema_last_updated
        self.score = score
        self.services = services
        self.services_score = services_score
        self.user_id = user_id
        self.venue_description = venue_description
        self.venue_score = venue_score
        self.vfm = vfm
        self.visit_again = visit_again
        self.DELIMITER = "|"


    def parse_value(self, value):
        if value is None:
            return "None"
        return value

    def parse_and_clean_value(self, value):
        if value is None:
            return "None"
        return value.replace("\r\n", "\\r\\n").replace("\n", "\\n").replace("\r", "\\r")


    def generate_record(self):
        return "".join([self.parse_value(self.id) + self.DELIMITER,
                        self.parse_value(self.user_id) + self.DELIMITER,
                        self.parse_and_clean_value(self.nickname) + self.DELIMITER,
                        self.parse_and_clean_value(self.candidate_description) + self.DELIMITER,
                        self.parse_value(self.candidate_description_score) + self.DELIMITER,
                        self.parse_and_clean_value(self.client_nickname) + self.DELIMITER,
                        self.parse_and_clean_value(self.comments) + self.DELIMITER,
                        self.parse_value(self.comments_score) + self.DELIMITER,
                        self.parse_value(self.create_date) + self.DELIMITER,
                        self.parse_value(self.exclude_affiliate) + self.DELIMITER,
                        self.parse_and_clean_value(self.fee) + self.DELIMITER,
                        self.parse_and_clean_value(self.location) + self.DELIMITER,
                        self.parse_value(self.meet_date) + self.DELIMITER,
                        self.parse_and_clean_value(self.meet_duration) + self.DELIMITER,
                        self.parse_value(self.oncall) + self.DELIMITER,
                        self.parse_and_clean_value(self.personality) + self.DELIMITER,
                        self.parse_value(self.personality_score) + self.DELIMITER,
                        self.parse_value(self.rating_total) + self.DELIMITER,
                        self.parse_value(self.recommend) + self.DELIMITER,
                        self.parse_value(self.rejected) + self.DELIMITER,
                        self.parse_and_clean_value(self.report_rating) + self.DELIMITER,
                        self.parse_value(self.schema_id) + self.DELIMITER,
                        self.parse_value(self.schema_last_updated) + self.DELIMITER,
                        self.parse_value(self.score) + self.DELIMITER,
                        self.parse_and_clean_value(self.services) + self.DELIMITER,
                        self.parse_value(self.services_score) + self.DELIMITER,
                        self.parse_and_clean_value(self.venue_description) + self.DELIMITER,
                        self.parse_value(self.venue_score) + self.DELIMITER,
                        self.parse_and_clean_value(self.vfm) + self.DELIMITER,
                        self.parse_value(self.visit_again)])


class PhoenixServiceReportV2Loader:

    def __init__(self):
        # initialise directories
        self.reports_feed_directory = ".././app-data/feeds-servicereportsv2-phoenix"
        self.global_reports_feed_directory = ".././app-data/feeds-servicereportsv2-phoenix/global"
        if not os.path.exists(self.reports_feed_directory):
            os.makedirs(self.reports_feed_directory, exist_ok=True)
        if not os.path.exists(self.global_reports_feed_directory):
            os.makedirs(self.global_reports_feed_directory, exist_ok=True)


    """
    This is a common function. Refactor this.
    """

    def get_number_of_records(self, file_path):
        f = open(file_path, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        return len(lines)


    """
    This should be a common function. Refactor this.
    """
    def extractUserId(self, text):
        res = re.search("userID\\=([0-9]+)", text)
        return res.group(1)




    """
    This should be a common function. Refactor this.
    """
    def read_global_userid_list(self):
        global_userid_list_path = ".././app-data/static/global-userid-list.txt"
        f = open(global_userid_list_path, 'r', encoding='utf-8')
        user_id_list = f.readlines()
        f.close()
        return user_id_list

    """
    This should be a common function. Refactor this.
    """
    def read_profile_urls_from_userlist_temp_file(self):
        temp_userlist_feed_file_path = ".././app-data/temp/temp_userlist_" + datetime.datetime.now().strftime(
            "%Y-%m-%d") + ".txt"
        f = open(temp_userlist_feed_file_path, 'r', encoding='utf-8')
        urls = f.readlines()
        f.close()
        return urls

    def generate_feed_file(self, records, user_id, page_number, isGlobal):
        file_name = "/feeds-servicereportsv2-phoenix_" + str(user_id) + "_" + datetime.datetime.now().strftime(
            "%Y-%m-%d") + "_" + str(page_number) + ".txt"
        if isGlobal:
            feed_file_path = self.global_reports_feed_directory + file_name
        else:
            today_feed_dir = self.reports_feed_directory + "/" + datetime.datetime.now().strftime("%Y-%m-%d")
            if not os.path.exists(today_feed_dir):
                os.makedirs(today_feed_dir, exist_ok=True)
            feed_file_path = today_feed_dir + "/" + file_name
        f = open(feed_file_path, 'w', encoding="utf-8")
        for r in records:
            f.write(r.generate_record() + "\n")
        f.close()

    def update_temp_file(self, user_id, isGlobal):
        if isGlobal:
            temp_file_path = ".././app-data/temp/temp_servicereports-v2_global.txt"
        else:
            temp_file_path = ".././app-data/temp/temp_servicereports-v2_" + datetime.datetime.now().strftime(
                "%Y-%m-%d") + ".txt"
        if not os.path.exists(temp_file_path):
            f = open(temp_file_path, 'w', encoding="utf-8")
            f.write(user_id + "\n")
            f.close()
        else:
            f = open(temp_file_path, 'a', encoding="utf-8")
            f.write(str(user_id) + "\n")
            f.close()

    """
    This should be a common function. Refactor
    """

    def read_user_ids_from_temp_feedback_file(self, isGlobal):
        if isGlobal:
            temp_feed_file_path = ".././app-data/temp/temp_servicereports-v2_global.txt"
        else:
            temp_feed_file_path = ".././app-data/temp/temp_servicereports-v2_" + datetime.datetime.now().strftime(
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

    def parse_feed(self, user_id, isGlobal):
        response = self.connect(user_id, 1)
        if response.status_code != 200:
            print("[ERROR] Unable to retrieve feed data for user [" + str(user_id) + "]. Error code : " + str(response.status_code))
            return
        data = response.json()
        # number of reports:
        number_of_reports = data["results"][0]["found"]
        number_of_pages = loader.determine_number_of_pages(number_of_reports)

        if number_of_reports == 0:
            print("[WARN] No reports exist for this user [" + str(user_id) + "].")
        elif number_of_reports > 0 and number_of_pages == 1:
            print("[INFO] Loading service report for user: [" + str(user_id) + "], Reports : " + str(number_of_reports) + ", Pages:[" + str(number_of_pages) + "], Page 1")
            records = self.parse_data(data)
            self.generate_feed_file(records, user_id, 1, isGlobal)
        elif number_of_reports > 0 and number_of_pages > 1:
            print("[INFO] Loading service report for user: [" + str(user_id) + "], Reports: " + str(number_of_reports) + ", Pages : [" + str(number_of_pages) + "], Page 1")
            # get the first page, which is already loaded in memory
            records = self.parse_data(data)
            self.generate_feed_file(records, user_id, 1, isGlobal)
            # now loop through the remaining pages
            for i in range(2, number_of_pages + 1):
                # setup the request
                response = self.connect(user_id, i)
                if response.status_code == 200 or response.status_code == 201:
                    print("[INFO] Loading service report for user: [" + str(user_id) + "], Reports: " + str(
                        number_of_reports) + ", Pages : [" + str(number_of_pages) + "], Page " +str(i))

                    response_payload = response.json()
                    records = self.parse_data(response_payload)
                    self.generate_feed_file(records, user_id, i, isGlobal)
                    time.sleep(5)
                else:
                    print("[ERROR] Error in reading feed : " + str(response.status_code))
        else:
            print("[WARN] Unknown branch conditional")
        self.update_temp_file(user_id, isGlobal)
        time.sleep(5)

    def parse_data(self, data):
        records = []
        for hit in data["results"][0]["hits"]:
            doc = hit["document"]
            service_report = ServiceReportFeed(doc.get("candidateDescription", None),
                                               str(doc.get("candidateDescriptionScore", None)),
                                               doc.get("clientNickname", None),
                                               doc.get("comments", None),
                                               str(doc.get("commentsScore", None)),
                                               str(doc.get("createdDate", None)),
                                               str(doc.get("excludeAffiliate", None)),
                                               doc.get("fee", None),
                                               doc.get("id",None),
                                               doc.get("location", None),
                                               str(doc.get("meetDate", None)),
                                               doc.get("meetDuration", None),
                                               doc.get("nickname", None),
                                               str(doc.get("onCall", None)),
                                               doc.get("personality", None),
                                               str(doc.get("personalityScore", None)),
                                               str(doc.get("ratingTotal", None)),
                                               str(doc.get("recommend", None)),
                                               str(doc.get("rejected", None)),
                                               doc.get("reportRating", None),
                                               doc.get("schemaId", None),
                                               doc.get("schemaLastUpdated", None),
                                               str(doc.get("score", None)),
                                               doc.get("services", None),
                                               str(doc.get("servicesScore", None)),
                                               str(doc.get("userId", None)),
                                               doc.get("venueDescription", None),
                                               str(doc.get("venueScore", None)),
                                               doc.get("vfm",None),
                                               str(doc.get("visitAgain", None))
                                               )
            records.append(service_report)
        return records

    def determine_number_of_pages(self, number_of_reports):
        reports_per_page = 15
        if number_of_reports <= reports_per_page:
            return 1
        else:
            return (number_of_reports // reports_per_page) + 1

    def connect(self, user_id, page_number):
        payload = {"searches": [{"num_typos": "0", "per_page": 15, "infix": "fallback", "query_by": "nickname",
                                 "sort_by": "createdDate:desc", "include_fields": "*",
                                 "filter_by": "userId:=" + str(user_id),
                                 "highlight_full_fields": "nickname", "collection": "FieldReports", "q": "*",
                                 "page": page_number}]}

        headers = {"Content-Type": "application/json",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                   "x-typesense-api-key": "<KEY>"}

        return requests.post("https://<VENDOR_URL>/multi_search", headers=headers, json=payload)


if __name__ == "__main__":

    isGlobal = False

    loader = PhoenixServiceReportV2Loader()

    res = sys.argv

    if len(sys.argv) > 1 and sys.argv[1] == "--stats":
        print("[INFO] Download service report statistics")

        userids_in_global_list = loader.get_number_of_records(".././app-data/static/global-userid-list.txt")
        userids_with_downloaded_reports = loader.get_number_of_records(".././app-data/temp/temp_servicereports-v2_global.txt")

        print("[INFO] Number of user ids in global list: " + str(userids_in_global_list))
        print("[INFO] Number of users with feedback downloaded: " + str(userids_with_downloaded_reports))
        print("[INFO] Remaining users to download feedback for: " + str(userids_in_global_list - userids_with_downloaded_reports))
        exit(0)

    elif len(sys.argv) > 1 and sys.argv[1] == "--global":
        # run the global logic
        isGlobal = True
        if not os.path.exists(".././app-data/static/global-userid-list.txt"):
            print("[ERROR] global-userid-list.txt cannot be found in static directory. Exiting.")
            exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "--userId":
        user_id = sys.argv[2]
        feedback_user_ids = user_ids = [line.rstrip("\n") for line in loader.read_user_ids_from_temp_feedback_file(False)]
        if user_id not in feedback_user_ids:
            loader.parse_feed(int(user_id), False)
        else:
            print("[INFO] Service report for user : " + user_id + " is already downloaded. Ignoring...")
        exit(0)

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
            print("[INFO] Service report for user : " + user_id + " is already downloaded. Ignoring...")
        else:
            loader.parse_feed(int(user_id), isGlobal)
