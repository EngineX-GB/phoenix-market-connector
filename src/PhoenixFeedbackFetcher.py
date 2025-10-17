# PhoenixFeedbackFetcher.py
# Usage:
# python PhoenixFeedbackFetcher.py --standard ( to read of the temp/temp_userlist_<yyyy-MM-dd>.txt file and get feedback data for each user)
# python PhoenixFeedbackFetcher.py --userId <userId> (fetch feedback for 1 specific user)

import requests
from bs4 import BeautifulSoup
import hashlib
import re
import os
import datetime

from model.Feedback import Feedback


class PhoenixFeedbackFetcher:

    def __init__(self, propertyManager):
        self.propertyManager = propertyManager
        self.RATING_VALUES = ("Positive", "Negative", "Neutral", "FeedbackOnly")
        self.DICT_FEEDBACK_RECORDS = {}
        self.FEEDBACK_URL_PREFIX = propertyManager.getProviderUrl() + "/dlgViewRatings.asp?userID="

    def initialise(self):
        if not os.path.exists(self.propertyManager.getFeedsFeedbackDirectory()):
            os.makedirs(self.propertyManager.getFeedsFeedbackDirectory())

    def extractUserId(self, text):
        res = re.search("userID\\=([0-9]+)", text)
        return res.group(1)

    def run(self, userId):
        collectedFeedbackMetadata = False
        # headers: to be set properly via a system config file:
        headers = {"user-agent": "Mozilla/5.0"}
        req = requests.get(self.FEEDBACK_URL_PREFIX + userId, headers=headers)
        if req.status_code != 200:
            print("[ERROR] feedback data fetch returns error code : " + str(req.status_code))
        pageSource = req.text
        soup = BeautifulSoup(pageSource, "html.parser")
        escortTable = soup.find("table", {"id": "tblEscort"})
        dictKeyTemp = "";  # stores the previously last dictionary key value that created a record
        if escortTable is not None:
            allRows = escortTable.find_all("tr")

            feedback = None
            rowNumber = 0
            for row in allRows:
                rowNumber = rowNumber + 1
                if row.find("th") is not None:
                    # This is a 'divider' between the rows (if the row <tr> contains a <th> as one of its child elements)
                    if feedback is None:
                        feedback = Feedback()
                    else:
                        record = feedback
                        # add the generated record to a dictionary:
                        dictKey = (hashlib.md5(record.generateRecord().encode('utf-8')).hexdigest())
                        self.DICT_FEEDBACK_RECORDS.update({dictKey: record})
                        dictKeyTemp = dictKey
                        feedback = None
                else:
                    if len(row.find_all("td")) == 4:
                        feedback = Feedback()  # for the next data collection cycle
                        rating = row.find_all("td")[0].text
                        username = row.find_all("td")[1].text
                        timestamp = row.find_all("td")[2].text
                        purpose = row.find_all("td")[3].text
                        userId = None
                        # get the userId of the user who submitted the feedback (if they exist)
                        if row.find_all("td")[1].find("a") is not None:
                            hrefValue = row.find_all("td")[1].find("a").get("href")
                            userId = re.search("UserID\\=([0-9]+)", hrefValue).group(1)
                        if feedback is not None:
                            feedback.rating = rating
                            feedback.username = username
                            feedback.userId = userId
                            feedback.timestamp = timestamp
                            feedback.purpose = purpose
                    if len(row.find_all("td")) == 2:
                        if feedback is not None and feedback.rating is not None:
                            feedbackText = row.find_all("td")[1].text
                            feedback.feedbackText = feedbackText
                            if rowNumber == len(allRows):
                                # because there is no divider (a row with a <th>) after the last feedback row
                                # we need to check if this is the last feedback row and then add it to the
                                # dictionary
                                dictKey = (hashlib.md5(feedback.generateRecord().encode('utf-8')).hexdigest())
                                self.DICT_FEEDBACK_RECORDS.update({dictKey: feedback})
                        elif feedback is None:
                            # this part is concerned with saving responses from the service provider
                            responseText = row.find_all("td")[1].text
                            # fetch the last dictKey
                            updatedRecord = self.DICT_FEEDBACK_RECORDS[dictKeyTemp]
                            updatedRecord.responseText = responseText
                            # update the dictionary, by removing the old entry and add it back as a new entry
                            # with a new computed hash (as an ID) for the new record
                            newDictKey = (hashlib.md5(updatedRecord.generateRecord().encode('utf-8')).hexdigest())
                            self.DICT_FEEDBACK_RECORDS.pop(dictKeyTemp)
                            self.DICT_FEEDBACK_RECORDS.update({newDictKey: updatedRecord})
        else:
            print("[WARN] No feedback data found for userId : " + userId)

    def generateFeed(self, userId):
        # create the feedback-feeds folder if it does not exist:
        feedbackFeedDirectory = self.propertyManager.getFeedsFeedbackDirectory() + "/" + datetime.datetime.now().strftime("%Y-%m-%d")
        if os.path.exists(feedbackFeedDirectory) == False:
            os.makedirs(feedbackFeedDirectory)

        # here, clean up the dictionary to remove any irrelevant records

        for k, v in list(self.DICT_FEEDBACK_RECORDS.items()):
            if v.rating is None or not v.rating.startswith(self.RATING_VALUES):
                # if the record does not start with a rating of positive, negative, neutral or feedbackOnly, then remove it from the dictionary
                del self.DICT_FEEDBACK_RECORDS[k]

        dictKeys = self.DICT_FEEDBACK_RECORDS.keys()

        if len(dictKeys) > 0:
            filename = feedbackFeedDirectory + "/" + "feeds-feedback-phoenix_" + userId + "_" + datetime.datetime.now().strftime(
                "%Y-%m-%d_%H%M%S") + ".txt"
            feedFile = open(filename, "w", encoding="utf-8")
            for key in dictKeys:
                record = self.DICT_FEEDBACK_RECORDS[key].generateRecord()
                if record.startswith(self.RATING_VALUES):
                    feedFile.write(key + "|" + record + "\n")
            feedFile.close()
            print("[INFO] Generated Feedback Feed for UserId : " + userId + " (" + str(len(dictKeys)) + " records)")
            self.addFeedbackEntryIntoTempFile(self.FEEDBACK_URL_PREFIX + userId, filename)

        else:
            self.addFeedbackEntryIntoTempFile(self.FEEDBACK_URL_PREFIX + userId, "<EMPTY>")

        # clear the dictionary for the next entry
        self.DICT_FEEDBACK_RECORDS.clear()

    def main(self, argList: list[str]):
        self.initialise()
        # load the dictionary with the files (against the userIds) that have been downloaded already
        userFeedbackEntries = self.readAllEntriesFromTempFile()
        if argList[0] == "--userId":
            if argList[0] is not None:
                userId = argList[2]
                self.run(userId)
                self.generateFeed(userId)
            else:
                print("[ERR] Please enter a user Id")
        elif argList[1] == "--standard":
            # read the list of users available today (from temp folder), extract the user IDs and then generate feedback feed
            todaysTempUserList = self.propertyManager.getTempDirectory() + "/temp_userlist_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt"
            if os.path.exists(todaysTempUserList):
                userListFile = open(todaysTempUserList, "r")
                lines = userListFile.read().splitlines()
                userListFile.close()
                for line in lines:
                    # extract the userId
                    userId = self.extractUserId(line)
                    if userId is not None:
                        self.run(userId)
                        self.generateFeed(userId)
                    else:
                        print("[ERR] User ID is null")
            else:
                print("[ERR] " + todaysTempUserList + " does not exist")
        elif argList[0] == "--advanced":
            # read the list of users available today (from temp folder), extract the user IDs and then generate feedback feed
            todaysTempUserList = self.propertyManager.getTempDirectory() + "/temp_userlist_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt"
            if os.path.exists(todaysTempUserList):
                userListFile = open(todaysTempUserList, "r")
                lines = userListFile.read().splitlines()
                userListFile.close()
                for line in lines:
                    # extract the userId
                    userId = self.extractUserId(line)
                    if userId is not None and userId not in userFeedbackEntries.keys():
                        self.run(userId)
                        self.generateFeed(userId)
            else:
                print("[ERR] " + todaysTempUserList + " does not exist")
        print("-----COMPLETED-----")

    def addFeedbackEntryIntoTempFile(self, url, feedbackFileName):
        tempFile = open(self.propertyManager.getTempDirectory() + "/temp_feedback_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt", "a",
                        encoding="utf-8")
        userId = self.extractUserId(url)
        tempFile.write(userId + "|" + feedbackFileName + "\n")
        tempFile.close()

    def readAllEntriesFromTempFile(self):
        tempFiles = {}
        if os.path.exists(self.propertyManager.getTempDirectory() + "/temp_feedback_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt"):
            tempFile = open(self.propertyManager.getTempDirectory() + "/temp_feedback_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt", "r",
                            encoding="utf-8")
            lines = tempFile.read().splitlines()
            for line in lines:
                fields = line.split("|")
                if tempFiles.get(fields[0]) is not None:
                    # the user id already exists in the dictionary and also has a second file:
                    tempFiles.get(fields[0]).add(fields[1])
                else:
                    if fields[1] == "<EMPTY>":
                        tempFiles.update({fields[0]: {}})
                    else:
                        tempFiles.update({fields[0]: {fields[1]}})  # userId, feedbackFilename
            tempFile.close()
            print("Number of entries in feedback temp file: " + str(len(tempFiles)))
        else:
            print("[WARN] No entries in the feedback temp file. Returning empty dictionary")
        return tempFiles
