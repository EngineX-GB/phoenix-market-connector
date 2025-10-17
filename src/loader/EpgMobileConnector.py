from loader.EpgTopicLoader import EpgTopicLoader
from datetime import datetime
import os
import re


class EpgMobileConnector:

    def __init__(self, propertyManager):
        self.propertyManager = propertyManager

    def extractUserId(self, text):
        res = re.search("userID\\=([0-9]+)", text)
        return res.group(1)

    # get the list of userIDs from the client temp list
    def getFileContentAsDistinctLines(self, filename):
        if os.path.exists(filename):
            f = open(filename, "r", encoding="utf-8")
            lines = set(f.read().splitlines())
            f.close()
            return lines
        else:
            return set()

    #  continue from here
    def loadUpAwUserIDAndEpgMapping(self, userIdsLinksToDownload):
        providerMapping = {}
        if os.path.exists(self.propertyManager.getStaticDirectory() + "/providermapping.txt"):
            f = open(self.propertyManager.getStaticDirectory() + "/providermapping.txt", "r", encoding="utf-8")
            lines = f.read().splitlines()
            f.close()
            userIds = []
            for userIdLink in userIdsLinksToDownload:
                userIds.append(self.extractUserId(userIdLink))
            # to continue
            for line in lines:
                fields = line.split(",")
                if fields[0] in userIds:
                    # add entry to the provider mapping dictionary
                    providerMapping.update({fields[0]: fields[1]})
        else:
            print("ERR> providermapping.txt does not exist")
        return providerMapping

    def updateTempEpgList(self, userIdLink, filepath):
        f = open(filepath, "a", encoding="utf-8")
        f.write(userIdLink + "\n")
        f.close()

    def generateFeedFile(self, userId, records, filepath):
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        else:
            f = open(filepath + "/feeds-feedback-epg_" + userId + "_" + datetime.now().strftime("%Y-%m-%d") + ".txt",
                     "w", encoding="utf-8")
            for rec in records:
                f.write(rec + "\n")
            f.close()
            print("Generated EPG Feedback for userId : [" + userId + "]")

    def main(self):

        if not os.path.exists(self.propertyManager.getFeedsFeedbackEpgDirectory() + "/"):
            os.makedirs(self.propertyManager.getFeedsFeedbackEpgDirectory() + "/")

        # check the temp_epg_client_yyyy-MM-dd.txt file to see if the user ratings have already been downloded for this user

        # read the providermapping file and collect the list of awUserIds -> serviceProviderId mappings into a collection

        # for each user, get the ratings
        # create the file for the user ratings

        # update a temp_epg_client_yyyy-MM-dd.txt file with the user id of the downloaded ratings

        clientTempFileName = self.propertyManager.getTempDirectory() +"/temp_userlist_" + datetime.now().strftime("%Y-%m-%d") + ".txt"
        epgTempFileName = self.propertyManager.getTempDirectory() + "/temp_epg_client_" + datetime.now().strftime("%Y-%m-%d") + ".txt"

        downloadedClientList = self.getFileContentAsDistinctLines(clientTempFileName)
        downloadedClientRatings = self.getFileContentAsDistinctLines(epgTempFileName)

        # determine the users who have ratings data to be downloaded
        userIdsLinksToDownload = downloadedClientList - downloadedClientRatings
        providerMapping = self.loadUpAwUserIDAndEpgMapping(userIdsLinksToDownload)

        print(clientTempFileName)
        print(epgTempFileName)

        print("[DEBUG] Number of users to download feedback for: " + str(len(userIdsLinksToDownload)))

        # use the provider mapping to get the service provider ID:

        print("[DEBUG] Size of AwUserId-to-ServiceProvider Mapper = " + str(len(providerMapping)))

        topicLoader = EpgTopicLoader()
        for userIdLink in userIdsLinksToDownload:
            userId = self.extractUserId(userIdLink)
            serviceProviderId = providerMapping.get(userId)
            if serviceProviderId is not None:
                content = topicLoader.getContentFeed(
                    self.propertyManager.getUkpUserProfileUrl() + serviceProviderId)
                topicRecords = topicLoader.extractRatingRecords(content, serviceProviderId, userId)
                # generate a file
                self.generateFeedFile(userId, topicRecords,
                                      self.propertyManager.getFeedsFeedbackEpgDirectory() + "/" + datetime.now().strftime("%Y-%m-%d"))
                # update the temp_epg_client file with this entry
                self.updateTempEpgList(userIdLink, epgTempFileName)
            else:
                self.updateTempEpgList(userIdLink, epgTempFileName)
