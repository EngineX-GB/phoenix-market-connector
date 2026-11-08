import json
import time

import requests


class PhoenixClientV2Loader:

    def __init__(self, propertyManager):
        self.propertyManager = propertyManager

    def connect(self, page_number, region):
        payload = {"searches":[{
            "num_typos": "0",
            "per_page": 48,
            "infix": "fallback",
            "query_by": "nickname, gender, enjoys, ethnicity, nationality, orientation",
            "include_fields": "acceptsSMS,allowRatings,acceptsWithheldCalls,accolades,age,avatarImageUrl,availableToday,country,county,disputes,escortIsFeatured,escortPriority,gender,hasTattoosOrPiercings,hideOnMap,localLocations,id,imageUrl,imageUrlGuest,imageBlurUrl,imageBlurUrlGuest,avatarImageBlurUrl,isBrandAmbassador,isContent,isDirectCam,isDirectCamOnline,isTrans,isVip,mainImageUrls,memberOfTheDayType,nationality,nickname,orientation,ratings,region,summary,town,userId,_geoloc",
            "sort_by": "escortPriority:desc,schemaId:asc",
            "highlight_full_fields": "nickname, gender, enjoys, ethnicity, nationality, orientation",
            "collection": "ProfileSearch",
            "q": "*",
            "facet_by": "allowRatings,availableToday,bodyType,breasts,bustSize,dayAvailability,dislikes,dressSize,enjoys,escortIsFeatured,escortOffers,excludeNationality,gender,hairColour,hasPhoneNumber,inBreaks,inCallRates.fourHour,inCallRates.halfHour,inCallRates.hour,inCallRates.hourHalf,inCallRates.overnight,inCallRates.quarterHour,inCallRates.threeHour,inCallRates.threeQuarterHour,inCallRates.twoHour,isDirectCamOnline,isVip,lastLoginGrouping,localLocations.lvl0,localLocations.lvl1,localLocations.lvl2,nationality,orientation,outBreaks,outCallRates.fourHour,outCallRates.halfHour,outCallRates.hour,outCallRates.hourHalf,outCallRates.overnight,outCallRates.quarterHour,outCallRates.threeHour,outCallRates.threeQuarterHour,outCallRates.twoHour,profileOffers,showMe,soloAndCouples,tattoosOrPiercingsGrouping,tattoosOrPiercingsVisibilityGrouping,withGenders",
            "filter_by": "bannedCountryIds:!=[158]&&isEscort:true&&escortIsLocalSearchFeatured:=[featured,localSearch,motd]&&showMe:=[Women] && escortOffers:=[`In+Calls+(Can+Accommodate)`] && availableToday:=[true] && showMe:=[`Women`] && localLocations.lvl1:=[`united-kingdom > " + region + "`]",
            "max_facet_values": 200,
            "page": page_number
        }]}

        headers = {"Content-Type": "application/json",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                   "x-typesense-api-key": self.propertyManager.getApiCred()}

        return requests.post(self.propertyManager.getTsApiProviderUrl() + "/multi_search", headers=headers,
                             json=payload)

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
