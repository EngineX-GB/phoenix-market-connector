import os
import sys

from loader.EpgMobileConnector import EpgMobileConnector
from loader.EpgServiceProviderLoader import EpgServiceProviderLoader
from portable.HtmlGenerator import HtmlGenerator
from loader.PhoenixFeedbackFetcher import PhoenixFeedbackFetcher
from loader.PhoenixImageFetcher import PhoenixImageFetcher
from portable.WatchListManager import WatchListManager
from util.PhoenixUtil import PhoenixUtil
from util.PropertyFileReader import PropertyFileReader
from model.PropertyManager import PropertyManager
from loader.PhoenixMobileConnector import PhoenixMobileConnector
from persistence.PersistenceIO import PersistenceIO

propertyFileReader = PropertyFileReader(".././properties/config.properties")
propertyManager = PropertyManager(propertyFileReader)
persistence = PersistenceIO(propertyManager)
connector = PhoenixMobileConnector(propertyManager, persistence)


# initialise some basic things that need to exist before starting.

# setup the static folder and add an empty watchlist file and providermapping file
if not os.path.exists(propertyManager.getStaticDirectory()):
    os.makedirs(propertyManager.getStaticDirectory(), exist_ok=True)
    open(propertyManager.getStaticDirectory() + "/providermapping.txt", "w").close()
    open(propertyManager.getStaticDirectory() + "/watchlist.txt", "w").close()

try:
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            r2 = propertyManager.getRequestPayloadNext().replace("${region.id}", "1").replace("${page.number}", "9999")  
            print(r2)
            pass
        elif sys.argv[1] == "stats":
            # get region (client data stats)
            connector.getNumberOfPagesPerRegion()
        elif sys.argv[1] == "details":
            # get region (client data stats)
            connector.getApplicationDetails()
        elif sys.argv[1] == "userIds":
            if len(sys.argv) > 2:
                userIdsParameter = sys.argv[2]
                userIdsList = userIdsParameter.split(",")
                connector.start()
                connector.processCustomUserSearch(userIdsList)
            else:
                print("[ERROR] No user ids defined.")
        elif sys.argv[1] == "region":
            if sys.argv[3] == "page":
                connector.start()
                connector.extractPageData(sys.argv[2], int(sys.argv[4]))
            elif sys.argv[3] == "start" and sys.argv[5] == "end":
                connector.start()
                connector.extractPageDataByPageRange(sys.argv[2], int(sys.argv[4]), int(sys.argv[6]))
        elif sys.argv[1] == "loadList":
            if len(sys.argv) > 2:
                resource = sys.argv[2]
                userIdList = []
                f = open(resource, "r", encoding="utf-8")
                entries = f.read().splitlines()
                for e in entries:
                    # extract the URLs:
                    userId = PhoenixUtil.extractUserId(e)
                    userIdList.append(userId)
                connector.start()
                connector.processCustomUserSearch(userIdList)
            else:
                print("[ERROR] No resource file defined.")
        elif sys.argv[1] == "watchlist":
            userIdList = []
            watchlistManager = WatchListManager(propertyManager)
            if len(sys.argv) > 2:
                userIdList.append(sys.argv[2])
            watchlistManager.main(userIdList)
        elif sys.argv[1] == "report":
            dateList = []
            if len(sys.argv) > 2:
                dateList.append(sys.argv[2])
            htmlGenerator = HtmlGenerator(propertyManager)
            htmlGenerator.main(dateList)
        elif sys.argv[1] == "sp-update":
            serviceProviderLoader = EpgServiceProviderLoader(propertyManager)
            endPageNumber = int(sys.argv[2])
            serviceProviderLoader.main(endPageNumber)
        elif sys.argv[1] == "get-ratings":
            epgMobileConnector = EpgMobileConnector(propertyManager)
            epgMobileConnector.main()
        elif sys.argv[1] == "feedback":
            feedbackFetcher = PhoenixFeedbackFetcher(propertyManager)
            argList = [sys.argv[1]]
            if len(sys.argv) == 3:
                argList.append(sys.argv[2])
            if len(sys.argv) == 4:
                argList.append(sys.argv[2])
                argList.append(sys.argv[3])
            feedbackFetcher.main(argList)
        elif sys.argv[1] == "image":
            imageFetcher = PhoenixImageFetcher(propertyManager)
            argList = [sys.argv[2]]
            if len(sys.argv) == 4:
                argList.append(sys.argv[3])
            imageFetcher.main(argList)
        else:
            connector.start()
            print("[INFO] Connect to service provider and generate feed file")
            # otherwise, this is in normal mode and the argument that must be accepted is the region code
            # e.g. 1 = UK, 2 = South East, etc.
            # sys.argv[1] will be the region code
            connector.main(sys.argv[1])
    else:
        print("[INFO] Connect to service provider and generate feed file")
        # set the region to UK (1) by default
        connector.main(str(1))
except KeyboardInterrupt:
    print("[INFO] Interrupted")
