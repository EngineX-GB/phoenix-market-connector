
# PHOENIX MOBILE CONNECTOR 2.0.0
#
# Run the script using either one of the following commands:
# python PhoenixMobileConnector.py              [normal mode - which downloads region 1 (London)]
#
# python PhoenixMobileConnector.py 2            [normal mode - a number that represents the region code]
#
# python PhoenixMobileConnector.py test         [test mode]
# 
# This requires the following libraries to be installed via PIP
#
# pip install requests
# pip install beautifulsoup4


import requests
import re
import sys
from bs4 import BeautifulSoup
import datetime
import json
from model.PhoenixClient import PhoenixClient
from util.PhoenixUtil import PhoenixUtil

class PhoenixMobileConnector:

    def __init__(self, propertyManager, IPersistence):
        self.persistence = IPersistence
        self.propertyManager = propertyManager

    def start(self):
        self.persistence.start()

    def connectAndRetrieve(self, payload):
        headers = PhoenixUtil.readHeaderData(self.propertyManager.getHeadersJsonFilePath())
        r = requests.post(self.propertyManager.getProviderUrl() + "/search.asp", data=payload, headers=headers)
        return r

    def extractUserProfiles(self, content):
        # contains the list of user IDs
        userIds = re.findall("sU\(([\(0-9\)]+)", content)
        user_profile_pages = []
        for userid in userIds:
            user_profile_pages.append(self.propertyManager.getProviderUrl() + "/viewProfile.asp?userID=" + userid)
        return user_profile_pages

    def getProfileDetails(self, userList):
        clientRecords = []
        try:
            for u in userList:
                pageUrl = u
                headers = PhoenixUtil.readHeaderData(self.propertyManager.getHeadersJsonFilePath())
                req = requests.get(pageUrl, headers=headers)
                pageSource = req.text
                rec = self.readProfileData(pageSource, u)
                if rec is None:
                    print("[WARN] Identified NULL Client reference for [" + pageUrl+ "]")
                else:
                    clientRecords.append(rec)
            return clientRecords
        except (KeyboardInterrupt, requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            print("[WARN] Ending script due to interrupt signal....Records captured : "+str(len(clientRecords)))
            self.persistence.save(clientRecords)
            # update the filter userid list
            urls = []
            for c in clientRecords:
                # get URLS for the filter list file
                urls.append(c.urlPage)
            self.persistence.updateUserTempDataFile(urls)
            sys.exit(0)

    def readProfileData(self, htmlSource, profileUrl):
        client = PhoenixClient()
        soup = BeautifulSoup(htmlSource, "html.parser")
        nameNode = soup.find("span", {"itemprop" : "name"})
        if nameNode is not None:
            name = nameNode.text
            isAvailableTodayNode = soup.find("td", {"style" : "font-weight: bold; color: green"})
            if isAvailableTodayNode is not None and "Available Today" in isAvailableTodayNode.text:
                print( "[" + isAvailableTodayNode.text + "]   " + name)
                if soup.find("img", {"alt" : "Member Verified"}) is not None:
                    client.verified = True
                client.userName = name
                userId = PhoenixUtil.extractUserId(profileUrl)
                client.userId = userId
                userPage = profileUrl
                client.urlPage = userPage

                links = soup.find_all("a")
                for a in links:
                    if ("Rating:" in a.text):
                        res = re.search("Rating:\\s([\\-,0-9]+)", a.text)
                        if (res.group(1) is not None):
                            rating = res.group(1)
                            client.rating = rating

                addressRegion = soup.find("td", {"itemprop":"addressRegion"})
                client.region = PhoenixUtil.checkNodeAndReturnValue(addressRegion, "text")
                addressCountry = soup.find("td", {"itemprop":"addressCountry"})
                addressLocality = soup.find("td", {"itemprop":"addressLocality"})
                telephone = soup.find("b", {"itemprop" : "telephone"})
                client.location = PhoenixUtil.checkNodeAndReturnValue(addressLocality, "text")
                client.telephone = PhoenixUtil.checkNodeAndReturnValue(telephone, "text")
                gender = soup.find("td", {"itemprop":"gender"})   
                tdElements = soup.findAll("td")

                for td in tdElements:
                    if (td.text == "Age:"):
                        age = td.findNext('td').contents[0]
                        client.age = age
                    if (td.text == "Nationality:"):
                        nationality = td.findNext('td').contents[0]
                        client.nationality = nationality
                    if (td.text == "Region:"):
                        region = td.findNext('td').contents[0]
                        client.region = region
                    if (td.text == "Member Since:"):
                        memberSince = td.findNext('td').contents[0]
                        client.memberSince = memberSince
                    if (td.text == "Ethnicity:"):
                        ethnicity = td.findNext('td').contents[0]
                        client.ethnicity = ethnicity
                    if (td.text == "Dress Size:"):
                        dressSize = td.findNext('td').contents[0]
                        client.dressSize = dressSize
                    if (td.text == "Eye Colour:"):
                        eyeColour = td.findNext('td').contents[0]
                        client.eyeColour = eyeColour
                    if (td.text == "Hair Colour:"):
                        hairColour = td.findNext('td').contents[0]
                        client.hairColour = hairColour
                    if (td.text == "Height:"):
                        height = td.findNext('td').contents[0]
                        client.height = PhoenixUtil.convertHeight(height)

                # code to get the service preferences
                # 2022-11-05 temporarily removed this for now. Will uncomment later
                # 2025-07-27 code has been uncommented

                preferenceList = []
                preferencesNode = soup.find("div", {"id" : "dPref"})
                if preferencesNode is not None and preferencesNode.find("table") is not None:
                    tableNode = preferencesNode.find("table")
                    preferenceElements = tableNode.findAll("td", {"class" : "Padded"})
                    for pref in preferenceElements:
                        preferenceList.append(pref.text)
                    client.preferenceList = json.dumps(preferenceList)

                # get email
                emailNode = soup.find("a", {"itemprop":"email"})
                if emailNode is not None:
                    client.email = emailNode.text

                rate15Min = PhoenixUtil.checkNodeAndReturnValue(soup.find(id="tdRI0.25"), "integer")
                rate30Min = PhoenixUtil.checkNodeAndReturnValue(soup.find(id="tdRI0.5"), "integer")
                rate45Min = PhoenixUtil.checkNodeAndReturnValue(soup.find(id="tdRI0.75"), "integer")
                rate1Hour = PhoenixUtil.checkNodeAndReturnValue(soup.find(id="tdRI1"), "integer")
                rate1HalfHour = PhoenixUtil.checkNodeAndReturnValue(soup.find(id="tdRI1.5"), "integer")
                rate2Hour = PhoenixUtil.checkNodeAndReturnValue(soup.find(id="tdRI2"), "integer")
                rate2HalfHour = PhoenixUtil.checkNodeAndReturnValue(soup.find(id="tdRI2.5"), "integer")
                rate3Hour = PhoenixUtil.checkNodeAndReturnValue(soup.find(id="tdRI3"), "integer")
                rate3HalfHour = PhoenixUtil.checkNodeAndReturnValue(soup.find(id="tdRI3.5"), "integer")
                rate4Hour = PhoenixUtil.checkNodeAndReturnValue(soup.find(id="tdRI4"), "integer")
                rateOvernight = PhoenixUtil.checkNodeAndReturnValue(soup.find(id="tdRI10"), "integer")
                client.rate15Min = rate15Min
                client.rate30Min = rate30Min
                client.rate45Min = rate45Min
                client.rate1Hour = rate1Hour
                client.rate1HalfHour = rate1HalfHour
                client.rate2Hour = rate2Hour
                client.rate2HalfHour = rate2HalfHour
                client.rate3Hour = rate3Hour
                client.rate3HalfHour = rate3HalfHour
                client.rate4Hour = rate4Hour
                client.rateOvernight = rateOvernight
                client.refreshTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return client

    def getNumberOfPagesPerRegion(self):
        statsMap = {}
        print("[INFO] Number of Pages of Client Data available Per Region")
        maxPageNumber = 14
        for region in range(1, maxPageNumber + 1):
            if region != 13:
                requestPayload = self.propertyManager.getRequestPayload().replace("${region.id}", str(region))
                response = self.connectAndRetrieve(requestPayload)
                if response is None:
                    print("[ERROR] - the response is null. Therefore, cannot process further")
                else:
                    res = response.text
                    totalNumberOfPages = self.extractNumberOfPagesInSearchResults(res, region)
                    statsMap[region] = totalNumberOfPages
        return statsMap

    def main(self, region):
        print("[INFO] Retrieving data for Region " + str(region))
        # page 0 (i.e page 1)
        requestPayload = self.propertyManager.getRequestPayload().replace("${region.id}", region)
        response = self.connectAndRetrieve(requestPayload)
        if response is None:
            print("[ERROR] - the response is null. Therefore, cannot process further")
        else:
            res = response.text
            # here, get the number of pages shown on the first search result page
            totalNumberOfPages = self.extractNumberOfPagesInSearchResults(res, str(region))
            self.processSearchResults(res)
            if totalNumberOfPages > 1:
                for pageNumber in range(1, totalNumberOfPages):     #page 1 onwards (i.e page 2 onwards)
                    print("[INFO] Loading page " + str(pageNumber) + " of " + str(totalNumberOfPages) + " for Region " + str(region))
                    # todo: extract the following lines replace them using the extractPageData()
                    newRequestPayload = self.propertyManager.getRequestPayloadNext().replace("${region.id}", region).replace("${page.number}", str(pageNumber))     
                    response = self.connectAndRetrieve(newRequestPayload)
                    self.processSearchResults(response.text)
                    # todo: =========
                    pageNumber+=1
            print("[INFO] Completed")


    # 0 = page 1
    # 1 = page 2
    # ..etc
    def extractPageData(self, region, pageNumber):
        newRequestPayload = self.propertyManager.getRequestPayloadNext().replace("${region.id}", region).replace("${page.number}", str(pageNumber))     
        response = self.connectAndRetrieve(newRequestPayload)
        self.processSearchResults(response.text)

    def extractPageDataByPageRange(self, region, startPageNumber, endPageNumber):
        endPageNumber = endPageNumber + 1 # upto and include the page number within the page range (have to add 1 to it)
        for pageNumber in range(startPageNumber, endPageNumber):
            print("Loading page " + str(pageNumber) + " of " + str(endPageNumber) + " for region " + region)
            self.extractPageData(region, pageNumber)

    def extractNumberOfPagesInSearchResults(self, text, region):
        numberOfPages = re.search("showing Page ([0-9]+) of ([0-9]+)", text)
        print("[INFO] Number of pages for region "+ str(region) + ": " + numberOfPages.group(2))
        return int(numberOfPages.group(2))


    def processSearchResults(self, res):
        userProfileList = self.extractUserProfiles(res)
        # here filter the list to only process user profiles that have NOT been processed already (for today)
        userProfileList = self.persistence.getOutstandingUserProfiles(userProfileList)
        # here invoke a method to loop through the profiles
        records = self.getProfileDetails(userProfileList)
        # generate the feed file
        if len(records) > 0:
            self.persistence.save(records)
        # update the list of users that you've already downloaded data for
        self.persistence.updateUserTempDataFile(userProfileList)


    '''
    This method is for taking in a list of userIds and checking to see if the users are
    available or not (i.e. custom data loads)
    '''
    def processCustomUserSearch(self, userIdList):
        # convert the list of userIds in the userIdList into a list of URLs
        userProfileList = []
        for userId in userIdList:
            url = self.propertyManager.getProviderUrl() + "/viewProfile.asp?userID=" + userId
            userProfileList.append(url)
        # here filter the list to only process user profiles that have NOT been processed already (for today)
        userProfileList = self.persistence.getOutstandingUserProfiles(userProfileList)
        # here invoke a method to loop through the profiles
        records = self.getProfileDetails(userProfileList)
        # generate the feed file
        if len(records) > 0:
            self.persistence.save(records)
        # update the list of users that you've already downloaded data for
        userProfileList.clear()
        for r in records:
            userProfileList.append(r.urlPage)

        self.persistence.updateUserTempDataFile(userProfileList)

    def getApplicationDetails(self):
        # read the app.json file
        # Note that needs to be fixed based on the where the cmd prompt is running from a particular directory
        # as run.sh run from the scripts folder.
        f = open("app.json")
        appConfig = json.load(f)
        f.close()
        print("[INFO] Application : " + appConfig["application"])
        print("[INFO] Version : " + appConfig["version"])
        print("[INFO] Date : " + appConfig["date"])
        if len(appConfig["changeset"]) > 0:
            print("[INFO] Changeset: ")
            for entry in appConfig["changeset"]:
                print("[INFO] " + entry)

        