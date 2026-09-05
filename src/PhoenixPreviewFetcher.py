import json
import time
from datetime import datetime, timedelta

import requests

from PhoenixAbstractV2DataLoader import PhoenixAbstractV2DataLoader
from model.Preview import Preview, PreviewCollapsedLine, PreviewDataHolder, PreviewExpandedLine


class PhoenixPreviewFetcher(PhoenixAbstractV2DataLoader):

    def __init__(self, propertyManager):
        super().__init__()
        self.propertyManager = propertyManager

    def load(self, data):
        preview_headers = []
        preview_collapsed_lines = []
        preview_expanded_lines = []
        results = data["Result"]
        for result in results:
            user_id = result["userId"]
            title = str(result["title"])
            details = str(result["details"])
            #datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
            start_date = result["startDate"]
            end_date = result["endDate"]
            is_active = str(result["isActive"])
            business_key = str(user_id) + "_" + start_date + "_" + end_date + "_" + str(is_active)

            preview_headers.append(Preview(str(user_id), title, details, start_date,
                                           end_date, str(is_active), business_key))

            # get the number of stops on the preview
            stops = result["stops"]
            for stop in stops:
                country = stop["country"]
                region = stop["region"]
                county = stop["county"]
                town = stop["town"]
                postcode = stop["postCode"]
                details = str(stop["details"])
                start_date = stop["startDate"]
                end_date = stop["endDate"]
                #
                # start_date_converted = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
                # end_date_converted = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")

                preview_collapsed_lines.append(PreviewCollapsedLine(str(user_id), country, region, county, town,
                                                                    postcode, details, start_date, end_date,
                                                                    business_key))

            # now take the "collapsed" preview lines (with start date and end date) and break up the line to
            # individual dates, where each line is a date of which the user is available within the start and end
            # date range.

            for line in preview_collapsed_lines:
                _start_date = datetime.strptime(line.start_date, "%Y-%m-%dT%H:%M:%S").date()
                _end_date = datetime.strptime(line.end_date, "%Y-%m-%dT%H:%M:%S").date()

                _dates = []

                while _start_date <= _end_date:
                    preview_expanded_lines.append(
                        PreviewExpandedLine(line.user_id, line.country, line.region, line.county,
                                            line.town, line.postcode, line.details,
                                            _start_date.strftime("%Y-%m-%d"),
                                            line.business_key))
                    _start_date += timedelta(days=1)

        return PreviewDataHolder(preview_headers, preview_collapsed_lines, preview_expanded_lines)

    # This function is for reading off a user id list for the day
    def execute(self):
        user_profiles = self.read_profile_urls_from_userlist_temp_file()
        if len(user_profiles) > 0:
            # get the list of user_ids that have previews already downloaded for the day
            existing_user_id_list = self.read_user_ids_from_temp_feedback_file("preview", False)
            # then go through each user id and fetch the data
            for user_profile in user_profiles:
                user_id = self.extractUserId(user_profile)
                if user_id is not None and user_id not in existing_user_id_list:

                    headers = {"Content-Type": "application/json",
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}

                    response = requests.get(
                        f"{self.propertyManager.getApiProviderUrl()}/api/Content/Tour/{user_id}?v=2", headers=headers)

                    # add a pause here to control the rate of API invocation
                    time.sleep(1)
                    if response.status_code != 200:
                        print(
                            f"An error has occurred when fetching preview data for {user_id}. Status code: {response.status_code}")
                    else:
                        preview_data_holder = self.load(response.json())
                        if len(preview_data_holder.get_preview_header()) > 0:
                            # here, you can either put the data in a csv file, or if it's in service mode
                            # then send it to the ingestion service to store in the database

                            # here, we will just get the expanded rows (individual days)
                            print("===================")
                            for p in preview_data_holder.get_preview_expanded_lines():
                                print(p.generate_record())
                            print("===================")

                            # if successful, then update the temp list for preview files, so the same user data is not
                            # downloaded again
                            self.update_temp_file(user_id, False, "preview")
                            pass
                        else:
                            print(f"[INFO] No preview data found for {user_id}")
