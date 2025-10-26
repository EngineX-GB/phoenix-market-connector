# EPGMobileConnector.py
# Date: 25-07-2022

import requests
import re
import os

class EpgServiceProviderLoader:

    def __init__(self, propertyManager):
        self.propertyManager = propertyManager

    def extractAwUserId(self, serviceProviderId):
        req = requests.get(self.propertyManager.getUkpUserProfileUrl() + str(serviceProviderId))

        source = req.text
        awLink = re.search(self.propertyManager.getProviderUrl() + "/([0-9]+)", source)
        if awLink is not None:
            return awLink.group(1)
        else:
            return "-"

    def buildProviderToAwIdMapper(self, startPage, endPage):
        providerMapping = []
        for i in range(startPage, endPage):
            if self.extractAwUserId(i) != "-":
                print("[INFO] Creating entry for service provider [" + str(i) + "]")
                providerMapping.append(str(self.extractAwUserId(i)) + "," + str(i))
        return providerMapping

    def writeToFile(self, mappingList):
        f = open(self.propertyManager.getStaticDirectory() + "/providermapping.txt", "a", encoding="UTF-8")
        for m in mappingList:
            f.write(m + "\n")
        f.close()


    def getServiceProviderIdOfLastEntryInMapperFile(self):
        if not os.path.exists(self.propertyManager.getStaticDirectory() + "/providermapping.txt"):
            print("[WARN] providermapping.txt does not exist.")
            return 0
        else:
            f = open(self.propertyManager.getStaticDirectory() + "/providermapping.txt", "r", encoding="UTF-8")
            lines = f.read().splitlines()
            lastServiceProviderIDEntry = None
            for l in lines:
                lastServiceProviderIDEntry = l.split(",")[1]
            f.close()
            return int(lastServiceProviderIDEntry)

    def main(self, endpagenumber:int):
        endPage = endpagenumber

        lastServiceProviderIdEntry = self.getServiceProviderIdOfLastEntryInMapperFile()
        if lastServiceProviderIdEntry == 0:
            # then there is no providermapping.txt file created, meaning we need to start loading service
            # providers for the first time. You need to only specify the endPage value (the service provider ID)
            # you want to scan up to:

            mappingList = self.buildProviderToAwIdMapper(1, endPage)
            self.writeToFile(mappingList)

        else:
            # pick up from the last entry in the providermapping.txt file and get the service provider id
            # increment it by 1 and continue scanning up to the endPage value (the service provider ID)
            # you want to scan up to:
            lastServiceProviderIdEntry = lastServiceProviderIdEntry + 1
            mappingList = self.buildProviderToAwIdMapper(lastServiceProviderIdEntry, endPage)
            self.writeToFile(mappingList)