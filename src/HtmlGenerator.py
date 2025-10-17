import os
import datetime


class HtmlGenerator:

    def __init__(self, propertyManager):
        self.propertyManager = propertyManager

    def readHtmlTemplate(self, templateFilePath):
        f = open(templateFilePath, "r")
        template = f.read()
        f.close()
        return template

    def execute(self, dateString):
        watchListRecords = self.getWatchListRecords(self.propertyManager.getStaticDirectory() + "/watchlist.txt")
        listingHtml = self.readHtmlTemplate(".././src/template/listings.template")
        mainHtml = self.readHtmlTemplate(".././src/template/main.template")
        watchListHtml = self.readHtmlTemplate(".././src/template/listings.template")
        client_rows = ""
        watchlist_rows = ""
        client_row_count = 0
        watchlist_row_count = 0
        feedDirectoryPath = self.propertyManager.getFeedsDirectory() + "/" + dateString
        files = os.listdir(feedDirectoryPath)
        print("Scanning through feeds in " + feedDirectoryPath)
        for f in files:
            if "clients_" in f:
                # read the file contents, line by line, break the string and fetch the required values
                records = self.getClientDataFromFeedFile(feedDirectoryPath + "/" + f)
                matchedWatchListrecords = self.getMatchedWatchListClientDataFromFeedFile(feedDirectoryPath + "/" + f,
                                                                                         watchListRecords)
                for r in records:
                    client_rows += r
                    client_row_count += 1
                for w in matchedWatchListrecords:
                    watchlist_rows += w
                    watchlist_row_count += 1

        # generate the listing page
        listingPage = listingHtml.replace("${records}", client_rows)
        self.generateHtmlPage(self.propertyManager.getReportsDirectory() + "/listings.html", listingPage)

        # generate the watchlist page
        watchListPage = watchListHtml.replace("${records}", watchlist_rows)
        self.generateHtmlPage(self.propertyManager.getReportsDirectory() + "/watchlist.html", watchListPage)

        # generate the main page (containing the listing as the embedded object)
        mainPage = mainHtml.replace("${POSITION_COUNT}", str(client_row_count)).replace("${LOAD_DATE}",
                                                                                        dateString).replace(
            "${WATCHLIST_COUNT}", str(watchlist_row_count))
        self.generateHtmlPage(self.propertyManager.getReportsDirectory() + "/main.html", mainPage)

    def generateHtmlPage(self, file, html):
        if not os.path.exists(file):
            open(file, "w", encoding="utf-8").close()
        f = open(file, "w", encoding="utf-8")
        f.write(html)
        f.close()

    def getWatchListRecords(self, file):
        f = open(file, encoding="utf-8")
        lines = f.read().splitlines()
        f.close()
        return lines

    def getClientDataFromFeedFile(self, file):
        data = []
        f = open(file, encoding="utf-8")
        lines = f.readlines()
        f.close()
        for l in lines:
            fields = l.split("|")
            # fetch data based on positions
            # 2022-10-30: A bug exists where some of the feed files are showing "None". Therefore when doing
            # a row split, the number of fields will be 1 (i.e. only showing "None"). If a split of a line has multiple
            # fields then it is an actual genuine record of data.
            if len(fields) > 1:
                if fields[16] != "-" and fields[21] == "London" and fields[4] != "Not Specified":
                    userNameField = fields[0]
                    userId = fields[19]
                    if self.checkIfUserHasDownloadedImage(userId):
                        userNameField = "<a onclick=\"openWindow('imageviewer.html?userId=" + userId + "')\" href=\"#\">" + userNameField + "</a>"
                    if len(fields[2]) > 22:
                        fields[2] = (fields[2])[:22] + "..."
                    data.append(
                        "<tr><td>" + userNameField + "</td><td>" + fields[16] + "</td><td>" + fields[1] + "</td><td>" +
                        fields[4] + "</td><td>" + fields[3] + "</td><td>" + fields[2] + "</td><td>" + fields[
                            8] + "</td></tr>")
                # return list
        return data

    def checkIfUserHasDownloadedImage(self, userId):
        imagesDirectory = self.propertyManager.getImageDirectory()
        if os.path.exists(imagesDirectory + "/" + userId):
            return True
        else:
            return False

    def getMatchedWatchListClientDataFromFeedFile(self, file, watchListRecords):
        data = []
        f = open(file, encoding="utf-8")
        lines = f.readlines()
        f.close()
        for l in lines:
            fields = l.split("|")
            # fetch data based on positions
            if len(fields) > 1:
                if fields[16] != "-" and fields[21] == "London" and fields[4] != "Not Specified":
                    if len(fields[2]) > 22:
                        fields[2] = (fields[2])[:22] + "..."
                    if fields[17] in watchListRecords:
                        data.append(
                            "<tr><td>" + fields[0] + "</td><td>" + fields[16] + "</td><td>" + fields[1] + "</td><td>" +
                            fields[4] + "</td><td>" + fields[3] + "</td><td>" + fields[2] + "</td><td>" + fields[
                                8] + "</td></tr>")
                # return list
        return data

    def main(self, dateList: list[str]):
        if not os.path.exists(self.propertyManager.getReportsDirectory()):
            os.makedirs(self.propertyManager.getReportsDirectory())

        if len(dateList) == 0:
            # run for today
            todaysDateFormat = datetime.datetime.now().strftime("%Y-%m-%d")
            todaysFeedDirectory = self.propertyManager.getFeedsDirectory() + "/" + todaysDateFormat
            if not os.path.exists(todaysFeedDirectory):
                print("ERR> Directory : " + todaysFeedDirectory + " does not exist.")
            else:
                self.execute(todaysDateFormat)
        else:
            # take in a specific date in the argument, go to the feed folder (if it exists)
            # and generate the report
            self.execute(dateList[1])
