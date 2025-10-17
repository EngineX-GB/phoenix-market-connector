import os
import datetime

class WatchListManager:

    def __init__(self, propertyManager):
        self.propertyManager = propertyManager

    def showTodaysWatchList(self):
        watchListMatches = []
        f = open(self.propertyManager.getStaticDirectory() + "/watchlist.txt", encoding="utf-8")
        watchListLines = f.read().splitlines()
        f.close()
        todaysDate = datetime.datetime.now().strftime("%Y-%m-%d")
        f = open(self.propertyManager.getTempDirectory() + "/temp_userlist_" + todaysDate + ".txt")
        entryLines = f.read().splitlines()
        f.close()
        for entryLine in entryLines:
            if entryLine in watchListLines:
                watchListMatches.append(entryLine)
        # loop through todays feeds and fetch more data to display:
        files = os.listdir(self.propertyManager.getFeedsDirectory() + "/" + todaysDate)
        for file in files:
            rows = self.readFeedFile(self.propertyManager.getFeedsDirectory() + "/" + todaysDate + "/" + file)
            for row in rows:
                fields = row.split("|")
                if len(fields) > 1 and fields[17] in watchListMatches:
                    print(fields[0] + " | " + fields[1] + " | " + fields[2] + " | " + fields[16])


    def readFeedFile(self, file):
        f = open(file, "r", encoding="UTF-8")
        lines = f.read().splitlines()
        f.close()
        return lines




    def addEntryToWatchList(self, userId):
        f = open(self.propertyManager.getStaticDirectory() + "/watchlist.txt", encoding="utf-8")
        lines = f.read().splitlines()
        f.close()

        # append the ID to the existing set of userIds in the watchlist
        entry = self.propertyManager.getProviderUrl() + "/viewProfile.asp?userID=" + userId

        if entry not in lines:
            lines.append(self.propertyManager.getProviderUrl() + "/viewProfile.asp?userID=" + userId)
            print("[INFO] Added User id : "+ userId + " to the watchlist")
        else:
            print("[WARN] User id : " + userId + " already exists in the watchlist")

        # regenerate the watchlist with the new userId
        g = open(self.propertyManager.getStaticDirectory() + "/watchlist.txt", "w")
        for l in lines:
            g.write(str(l) + "\n")
        g.close()


    def main(self, list_of_user_ids : list[str]):
        if len(list_of_user_ids) >= 1:
            self.addEntryToWatchList(list_of_user_ids[0])
        else:
            self.showTodaysWatchList()

# main()
# main method was invoked here