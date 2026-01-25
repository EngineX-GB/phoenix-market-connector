import datetime
import os
import time

import requests

from model.ServiceReportFeed import ServiceReportFeed
from PhoenixAbstractV2DataLoader import PhoenixAbstractV2DataLoader
from model import PropertyManager


class PhoenixServiceReportV2Loader(PhoenixAbstractV2DataLoader):

    def __init__(self, propertyManager: PropertyManager):
        # initialise directories
        super().__init__()
        self.propertyManager = propertyManager
        self.reports_feed_directory = self.propertyManager.getFeedsServiceReportsV2Directory()
        self.global_reports_feed_directory = self.propertyManager.getFeedsServiceReportsV2Directory() + "/global"
        if not os.path.exists(self.reports_feed_directory):
            os.makedirs(self.reports_feed_directory, exist_ok=True)
        if not os.path.exists(self.global_reports_feed_directory):
            os.makedirs(self.global_reports_feed_directory, exist_ok=True)


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


    def parse_feed(self, user_id, isGlobal):
        response = self.connect(user_id, 1)
        if response.status_code != 200:
            print("[ERROR] Unable to retrieve feed data for user [" + str(user_id) + "]. Error code : " + str(response.status_code))
            return
        data = response.json()
        # number of reports:
        number_of_reports = data["results"][0]["found"]
        number_of_pages = self.determine_number_of_pages(number_of_reports)

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

            # now loop through the remaining pages (only if isGlobal is true)
            # otherwise if isGlobal is false (i.e. it's a standard daily feed) then get the one page only.
            if isGlobal:
                for i in range(2, number_of_pages + 1):
                    # setup the request
                    response = self.connect(user_id, i)
                    if response.status_code == 200 or response.status_code == 201:
                        print("[INFO] Loading service report for user: [" + str(user_id) + "], Reports: " + str(
                            number_of_reports) + ", Pages : [" + str(number_of_pages) + "], Page " +str(i))

                        response_payload = response.json()
                        records = self.parse_data(response_payload)
                        self.generate_feed_file(records, user_id, i, isGlobal)
                        time.sleep(1)
                    else:
                        print("[ERROR] Error in reading feed : " + str(response.status_code))
        else:
            print("[WARN] Unknown branch conditional")
        self.update_temp_file(user_id, isGlobal, "servicereports")
        time.sleep(1)

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
                   "x-typesense-api-key": self.propertyManager.getApiCred()}

        return requests.post(self.propertyManager.getTsApiProviderUrl() + "/multi_search", headers=headers, json=payload)

    def execute(self, args: list[str]):
        isGlobal = False

        if len(args) == 1 and args[0] == "--stats":
            print("[INFO] Download service report statistics")

            userids_in_global_list = self.get_number_of_records(self.propertyManager.getStaticDirectory() + "/global-userid-list.txt")
            userids_with_downloaded_reports = self.get_number_of_records(
                self.propertyManager.getTempDirectory() + "/temp_servicereports-v2_global.txt")

            print("[INFO] Number of user ids in global list: " + str(userids_in_global_list))
            print("[INFO] Number of users with reports downloaded: " + str(userids_with_downloaded_reports))
            print("[INFO] Remaining users to download reports for: " + str(
                userids_in_global_list - userids_with_downloaded_reports))
            exit(0)

        elif len(args) == 1 and args[0] == "--global":
            # run the global logic
            isGlobal = True
            if not os.path.exists(self.propertyManager.getStaticDirectory() + "/global-userid-list.txt"):
                print("[ERROR] global-userid-list.txt cannot be found in static directory. Exiting.")
                exit(1)
        elif len(args) > 1 and args[0] == "--userId":
            user_id = args[1]
            feedback_user_ids = user_ids = [line.rstrip("\n") for line in
                                            self.read_user_ids_from_temp_feedback_file("servicereports", False)]
            if user_id not in feedback_user_ids:
                self.parse_feed(int(user_id), False)
            else:
                print("[INFO] Service report for user : " + user_id + " is already downloaded. Ignoring...")
            exit(0)

        user_id_list = []
        if not isGlobal:
            feedback_user_ids = user_ids = [line.rstrip("\n") for line in
                                            self.read_user_ids_from_temp_feedback_file("servicereports", False)]

            # check if the ratings for the user have already been downloaded.
            # if so, then ignore this user and move onto the next

            user_list_urls = self.read_profile_urls_from_userlist_temp_file()

            for url in user_list_urls:
                userId = self.extractUserId(url)
                user_id_list.append(userId)

        else:
            feedback_user_ids = user_ids = [line.rstrip("\n") for line in
                                            self.read_user_ids_from_temp_feedback_file("servicereports", True)]
            user_id_list = [line.rstrip("\n") for line in self.read_global_userid_list()]

        for user_id in user_id_list:
            if user_id in feedback_user_ids:
                print("[INFO] Service report for user : " + user_id + " is already downloaded. Ignoring...")
            else:
                self.parse_feed(int(user_id), isGlobal)
