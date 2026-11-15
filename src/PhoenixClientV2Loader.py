import json
import time

import requests

from model.PhoenixClient import PhoenixClient


class PhoenixClientV2Loader:

    def __init__(self, propertyManager):
        self.propertyManager = propertyManager

    def connect(self, page_number, region):
        payload = {"searches": [{
            "num_typos": "0",
            "per_page": 48,
            "infix": "fallback",
            "query_by": "nickname, gender, enjoys, ethnicity, nationality, orientation",
            "include_fields": "availableToday,country,county,id,region,userId",
            "sort_by": "escortPriority:desc,schemaId:asc",
            "highlight_full_fields": "nickname, gender, enjoys, ethnicity, nationality, orientation",
            "collection": "ProfileSearch",
            "q": "*",
            "facet_by": self.propertyManager.getRequestPayloadFacetBy(),
            "filter_by": self.propertyManager.getRequestPayloadFilterBy().replace("{region}", region),
            "max_facet_values": 200,
            "page": page_number
        }]}

        headers = {"Content-Type": "application/json",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                   "x-typesense-api-key": self.propertyManager.getApiCred()}

        return requests.post(self.propertyManager.getTsApiProviderUrl() + "/multi_search", headers=headers,
                             json=payload)

    # To get the list of user ids of clients that are available today in the given region
    # parameters:
    #   region: the region string
    # return:
    #   the full list of user-ids for a given region
    def load(self, region):
        print(f"[INFO] Collecting active user ids for : {region}")
        final_user_id_set = set()
        max_number_of_pages = 30
        for i in range(1, max_number_of_pages):
            print(f"[INFO] Reading/collecting user id data on page {i}")
            res = self.connect(i, region)
            if res.status_code == 200:
                user_id_list = self.read_feed(res.json())
                if len(user_id_list) == 0:
                    print(f"[WARN] No user ids were collected. Ending collection for the region")
                    break
                final_user_id_set.update(user_id_list)
                time.sleep(2)
            else:
                print(f"[ERROR] Unable to fetch active user ids for loading. Status code : {res.status_code}")
                break
        print(f"[INFO] Number of user ids collected for {region} : {len(final_user_id_set)}")
        return final_user_id_set

    # To get the user profile data required for storage
    # parameters:
    #   user_id: the user_id of the client
    # return:
    #   PhoenixClient class containing the data
    def load_user_profile_data(self, user_id) -> PhoenixClient:
        client = PhoenixClient()
        with open("C:/Users/Dell/Documents/user-profile.json", encoding="UTF-8") as f:
            jsonData = json.load(f)
            client.userId = jsonData["Result"]["userId"]
            client.userName = jsonData["Result"]["nickname"]
            # registered date
            client.ethnicity = jsonData["Result"]["interview"]["ethnicity"]
            client.dressSize = jsonData["Result"]["interview"]["dressSize"]
            client.hairColour = jsonData["Result"]["interview"]["hairColour"]
            client.age = jsonData["Result"]["is"]["age"]
            client.gender = jsonData["Result"]["is"]["gender"]
            client.nationality = jsonData["Result"]["is"]["nationality"]
            client.location = jsonData["Result"]["location"]["town"]
            client.region = jsonData["Result"]["is"]["region"]
            client.preferenceList = json.dumps(jsonData["Result"]["preferences"]["enjoys"])
            # postcode (field that does not exist in the current model)
            # station (field that does not exist in the current model)
            # height
            client.rating = jsonData["Result"]["ratings"]["total"]
            client.eyeColour = client.dressSize = jsonData["Result"]["interview"]["eyeColour"]
            print(jsonData["Version"])
        return client

    def read_feed(self, json_data):
        user_id_set = set()
        count = 0
        # get the list of ids
        results = json_data["results"]
        firstResultSet = results[0]
        hits = firstResultSet["hits"]
        for hit in hits:
            id = hit["document"]["id"]
            # print(id)
            user_id_set.add(id)
            count = count + 1
        return user_id_set

    # this function is only used for local testing
    # i.e. if you had a file locally to test the parsing.
    def read_feed_from_file(self):
        with open("C:/payload.json", encoding="UTF-8") as f:
            json_data = json.load(f)
            # print(json_data)
            count = 0
            # get the list of ids
            results = json_data["results"]
            firstResultSet = results[0]
            hits = firstResultSet["hits"]
            for hit in hits:
                id = hit["document"]["id"]
                print(id)
                count = count + 1
            print("Count : " + str(count))


if __name__ == "__main__":
    c = PhoenixClientV2Loader(None)
    c.load_user_profile_data("123")
