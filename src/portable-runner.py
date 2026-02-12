import os
import sys

from loader.EpgMobileConnector import EpgMobileConnector
from loader.EpgServiceProviderLoader import EpgServiceProviderLoader
from portable.HtmlGenerator import HtmlGenerator
from loader.PhoenixFeedbackFetcher import PhoenixFeedbackFetcher
from loader.PhoenixImageFetcher import PhoenixImageFetcher
from portable.WatchListManager import WatchListManager
from PathController import PathController
from PhoenixServiceReportV2Loader import PhoenixServiceReportV2Loader
from PhoenixFeedbackV2Loader import PhoenixFeedbackV2Loader
from src.loader.PhoenixOrderLoader import PhoenixOrderLoader
from util.PhoenixUtil import PhoenixUtil
from util.PropertyFileReader import PropertyFileReader
from model.PropertyManager import PropertyManager
from loader.PhoenixMobileConnector import PhoenixMobileConnector
from persistence.PersistenceIO import PersistenceIO


def check_and_setup_default_properties():
    if not os.path.exists(".././properties/config.properties") or not os.path.exists(".././properties/headers.json"):
        print("[WARN] Required config files do not exist. Preparing setup to create default ones....")
        provider_domain_name = input("Enter the provider domain name: ")
        content_domain_name = input("Enter the content domain name: ")
        api_provider_domain_name = input("Enter the API provider domain name: ")
        ts_api_provider_domain_name = input("Enter the TS-API provider domain name: ")
        ukp_domain_name = input("Enter the UKP domain name: ")
        domain_properties_map = {"provider_domain_name": provider_domain_name,
                                 "content_domain_name": content_domain_name,
                                 "ukp_domain_name": ukp_domain_name,
                                 "api_provider_domain_name": api_provider_domain_name,
                                 "ts_api_provider_domain_name" : ts_api_provider_domain_name}

        create_default_properties(".././properties/config.properties", "template/config.properties.template", domain_properties_map)
        create_default_properties(".././properties/headers.json", "template/headers.json.template", domain_properties_map)
        create_default_properties(".././properties/api.headers.json", "template/api.headers.json.template", domain_properties_map)

def create_default_properties(config_file_path: str, template_file_path: str, domain_properties_map):
    if not os.path.exists(config_file_path):
        print("[WARN] " + config_file_path + " file does not exist. Creating a default one.")
        os.makedirs(".././properties", exist_ok=True)
        # read the template file
        config_template = open(PathController.resource_path(template_file_path), 'r', encoding='UTF-8')
        new_lines = list()
        lines = config_template.readlines()
        for line in lines:
            if "{provider.domain.name}" in line:
                line = line.replace("{provider.domain.name}", domain_properties_map["provider_domain_name"])
            if "{content2.domain.name}" in line:
                line = line.replace("{content2.domain.name}", domain_properties_map["content_domain_name"])
            if "{api.provider.domain.name}" in line:
                line = line.replace("{api.provider.domain.name}", domain_properties_map["api_provider_domain_name"])
            if "{ts.api.provider.domain.name}" in line:
                line = line.replace("{ts.api.provider.domain.name}", domain_properties_map["ts_api_provider_domain_name"])
            if "{ukp.domain.name}" in line:
                line = line.replace("{ukp.domain.name}", domain_properties_map["ukp_domain_name"])
            if line.startswith("request.payload="):
                line = line.replace("request.payload=", "").strip()
                r_line = line[::-1]
                line = "request.payload=" + str(r_line) + "\n"
            if line.startswith("api.cred="):
                line = line.replace("api.cred=", "").strip()
                r_line = line[::-1]
                line = "api.cred=" + str(r_line) + "\n"
            if line.startswith("request.payload.next="):
                line = line.replace("request.payload.next=", "").strip()
                r_line = line[::-1]
                line = "request.payload.next=" + str(r_line) +"\n"
            if "\"cookie\":" in line:
                line = line.replace("\"cookie\":", "").strip()
                r_line = line[::-1]
                line = "\t\"cookie\":  " + str(r_line) + "\n"
            new_lines.append(line)
        config_template.close()
        # create a new config file with the string interpolation
        config_file = open(config_file_path, 'w', encoding='utf-8')
        config_file.writelines(new_lines)
        config_file.close()


# Run this check to see if the required config files are present. If not, create them from scratch.
check_and_setup_default_properties()


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
        elif sys.argv[1] == "servicereports":
            serviceReportLoader = PhoenixServiceReportV2Loader(propertyManager)
            serviceReportLoader.execute([sys.argv[2]])
        elif sys.argv[1] == "feedbackv2":
            feedbackV2Loader = PhoenixFeedbackV2Loader(propertyManager)
            feedbackV2Loader.execute([sys.argv[2]])
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
        elif sys.argv[1] == "raise-order":
            order_loader = PhoenixOrderLoader(propertyManager)
            order_loader.execute(False)
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
