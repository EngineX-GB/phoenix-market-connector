from persistence.IPersistence import IPersistence
import os
from util.PhoenixUtil import PhoenixUtil
from model.PropertyManager import PropertyManager
import datetime

class PersistenceIO(IPersistence):
    
    def __init__(self, propertyManager):
        self.propertyManager = propertyManager

    def start(self):
        print("[INFO] Initialising script")
        if not os.path.exists(self.propertyManager.getFeedsDirectory()):
            os.makedirs(self.propertyManager.getFeedsDirectory())
        if not os.path.exists(self.propertyManager.getTempDirectory()):
            os.makedirs(self.propertyManager.getTempDirectory())
        todaysFeedFolderName = self.propertyManager.getFeedsDirectory() + "/" + PhoenixUtil.getTodaysDate()
        if not os.path.exists(todaysFeedFolderName):
            os.makedirs(todaysFeedFolderName)

    def save (self, records):
        print("[INFO] Generating feed file")
        f = open(self.propertyManager.getFeedsDirectory() + "/" +PhoenixUtil.getTodaysDate() + "/" + self.generateFileName(), "w", encoding="utf-8")
        for l in records:
            f.write(str(l.generateRecord()) + "\n")
        f.close()


    def generateFileName(self):
        return "clients_"+ datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".txt"

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

    def handleError (self, records):
        print("IO")
