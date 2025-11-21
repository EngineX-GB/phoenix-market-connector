import datetime
import json
import os
import requests


from persistence.PersistenceIO import PersistenceIO


class PersistenceNET(PersistenceIO):

    def __init__(self, propertyManager):
        super().__init__(propertyManager)

    def start(self):
        if not os.path.exists(self.propertyManager.getTempDirectory()):
            os.makedirs(self.propertyManager.getTempDirectory())

    def save (self, records: list):
        print("[INFO] Publish to external service for ingestion.")

        strRecords= []
        # the list of records will be of type PhoenixClient.
        # Convert to string before transferring over the wire.
        for r in records:
            strRecords.append(r.generateRecord())

        jsonRecords = json.dumps(strRecords)

        ingestionServiceEndpoint = self.propertyManager.getIngestionServiceEndpoint()

        response = requests.post(url=ingestionServiceEndpoint + "/clients", data=jsonRecords)
        if response.status_code != 201 and response.status_code != 200:
            print("[ERROR] Failed to publish records for ingestion. Error code : " + str(response.status_code))
        else:
            print("[INFO] Successfully published records for ingestion. Code : " + str(response.status_code))

    def generateTempFileName(self):
        return self.propertyManager.getTempDirectory() + "/temp_userlist_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt"

    def getOutstandingUserProfiles(self, userProfileUrlList):
        filename = self.generateTempFileName()
        if not os.path.exists(filename):
            open(filename, "w").close()
        f = open(filename, "r")
        lines = f.read().splitlines()
        f.close()
        print("[INFO] Entries in the profile list = " + str(len(lines)))
        userProfilesNotDownloaded = list(set(userProfileUrlList) - set(lines))
        print("[INFO] User profiles that must be downloaded = "+str(len(userProfilesNotDownloaded)))
        return userProfilesNotDownloaded

    def updateUserTempDataFile(self, urls):
        f = open(self.generateTempFileName(), "a")
        for l in urls:
            f.write(str(l) + "\n")
        f.close()
