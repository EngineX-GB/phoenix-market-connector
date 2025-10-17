import os
import datetime
import sys

@staticmethod
def convertHeight(heightInFoot):
    height = {"4\"0" : 0.0,
             "4\"1" : 0.0,
             "4\"2" : 0.0,
             "4\"3" : 0.0,
             "4\"4" : 0.0,
             "4\"5" : 0.0,
             "4\"6" : 0.0,
             "4\"7" : 0.0,
             "4\"8" : 0.0,
             "4\"9" : 0.0,
             "4\"10" : 0.0,
             "4\"11" : 0.0,
             "5\"0" : 0.0,
             "5\"1" : 0.0,
             "5\"2" : 0.0,
             "5\"3" : 0.0,
             "5\"4" : 0.0,
             "5\"5" : 0.0,
             "5\"6" : 0.0,
             "5\"7" : 0.0,
             "5\"8" : 0.0,
             "5\"8" : 0.0,
             "5\"9" : 0.0,
             "5\"10" : 0.0,
             "5\"11" : 0.0,
             "6\"0" : 0.0,
             "6\"1" : 0.0,
             "6\"2" : 0.0,
             "6\"3" : 0.0,
             "6\"4" : 0.0,
             "6\"5" : 0.0,
             "6\"6" : 0.0,
             "6\"7" : 0.0,
             "6\"8" : 0.0,
             "6\"9" : 0.0,
             "6\"10" : 0.0,
             "6\"11" : 0.0,
             }
    return height[heightInFoot]

def getFeedbackDataForUser(dateString, ratingFilter, userId):
    current_date_format_string = None
    if dateString is None or dateString == "today":
        current_date_format_string = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        current_date_format_string = dateString
    feedbackDirectory = "../feeds-feedback-phoenix" + "/" + current_date_format_string
    if os.path.exists(feedbackDirectory):
        feedbackFiles = os.listdir(feedbackDirectory)
        for f in feedbackFiles:
            if userId in f:
                # open the file
                openFeedbackFile(feedbackDirectory + "/" + f, ratingFilter)

    else:
        print("ERR> Directory [" + feedbackDirectory + "] not found")
    


def openFeedbackFile(filename, ratingFilter):
    f = open(filename, "r", encoding="utf-8")
    lines = f.read().splitlines()
    print("\n---------------------------------------\n")
    for l in lines:
        fields = l.split("|")
        if ratingFilter == fields[1]:
            print("Rating : " + fields[1])
            print("Date : " + fields[4])
            print("Comment: " + fields[6])
            if fields[7] != "None":
                print("Response : " + fields[7])
            print("\n---------------------------------------\n")
        elif ratingFilter == "ALL":
            print("Rating : " + fields[1])
            print("Date : " + fields[4])
            print("Comment: " + fields[6])
            if fields[7] != "None":
                print("Response : " + fields[7])
            print("\n---------------------------------------\n")
    f.close()


def listAllFeedDates():
    feedsDirectory = "../feeds"
    if os.path.exists(feedsDirectory):
        feedDirectories = os.listdir(feedsDirectory)
        for f in feedDirectories:
            print("[OUT] " + f + " (" + str(len(os.listdir(feedsDirectory + "/" + f))) +" files)")

def generateUserMasterFile():
    imagesDirectory = "../images"
    if os.path.exists(imagesDirectory):
        userImageDirectories = os.listdir(imagesDirectory)
        file = open("../temp/temp_image_master_file.txt", "w", encoding="UTF-8")
        for d in userImageDirectories:
            file.write(d + "\n")
        file.close()
        print("[INFO] Image master file is created")
    else:
        print("[ERROR] images directory does not exist.")



# Query existing feed files to find a client either by username or by provider UserID
def search(searchString, customDate):
    results = []
    feedDirectory = "../feeds/" + customDate;
    if os.path.exists(feedDirectory):
        files = os.listdir(feedDirectory)
        # loop though these files
        # open the stream of the files and capture suitable matches
        for f in files:
            readFile(feedDirectory + "/" + f, results, searchString)
    return results


def singleSearch (searchString, customDate):
    if customDate is None:
        current_date_format_string = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        current_date_format_string = customDate
    print("\n[INFO] Search through data as of " +current_date_format_string + "\n")
    results = search(searchString, current_date_format_string)
    # View the results list (to include the username, phone number and user ID)
    if len(results) > 0:
        for result in results:
            print(result+"\n")
        print("\n" +str(len(results)) + " result{s) found.")
    else:
        print("[INFO] No matches returned")
    print("\n")



def historySearch (searchString, numdays):
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
    for dateString in date_list:
        results = search(searchString, dateString.strftime("%Y-%m-%d"))
        if len(results) > 0:
            for result in results:
                print(result + "\n")


def readFile(filename, results, searchString):
    f = open(filename, "r", encoding="UTF-8")
    lines = f.read().splitlines()
    for l in lines:
        if searchString in l:
            # split the record to get the user ID, telephone number, Username, Region
            recordSplit = l.split("|")
            results.append(recordSplit[0] +" | " + recordSplit[1] + " | "  + recordSplit[3] + " | " + recordSplit[4] + " | "   + recordSplit[16] + " | " + recordSplit[19] + " | " + recordSplit[21])
    f.close()


def readFileDetectDuplicates(filename, dictCount, dictDuplicate, printFileNames, performFix):
    duplicateUserIds = set()
    f = open(filename, "r", encoding="utf-8")
    lines = f.read().splitlines()
    f.close()
    for l in lines:
        recordSplit = l.split("|")
        if len(recordSplit) > 1:        # to handle cases where the line in the feed shows 'None'
            if recordSplit[19] in dictCount:
                updatedCount = (dictCount[recordSplit[19]]) + 1
                dictCount[recordSplit[19]] = updatedCount
                duplicateUserIds.add(recordSplit[19])
                # append the name of the files that contain the duplicate
                if printFileNames is True:
                    print("[WARN] Identified duplicate in " + filename+ ", userId: " + recordSplit[19])
            else:
                dictCount[recordSplit[19]] = 1
    if performFix is True and len(duplicateUserIds) > 0:
        isFixed = removeDuplicates(filename, duplicateUserIds)
        if isFixed is True:
            print("[INFO] File : [" + filename + "] has been fixed")
        else:
            print("[INFO] File : [" + filename + "] has not been fixed. Please fix manually")

"""Attempts to fix the file and removes the duplicates"""
def removeDuplicates(filename, userIdSet):
    print("[INFO] Fixing the file : [" + filename + "] for user IDs: " + str(userIdSet))
    f = open(filename, "r", encoding="utf-8")
    currentLines = f.read().splitlines()
    f.close()
    # perform the fix
    newFile = open(filename, "w", encoding="utf-8")
    for cl in currentLines:
        fields = cl.split("|")
        if fields[19] not in userIdSet:
            newFile.write(cl + "\n")
    newFile.close()
    # confirm this in the new file
    f2 = open(filename, "r", encoding="utf-8")
    newLines = f2.read().splitlines()
    f2.close()
    if len(newLines) < len(currentLines):
        return True
    else:
        return False


"""Method to detect duplicate records in feed files

    printFileNames: boolean
    printSummary: boolean
    performFix: boolean
    dateString: string

"""
def identifyDuplicateUserData(dateString, printFileNames, printSummary, performFix):
    path = ".././feeds/" + dateString
    dictCount = {}
    dictDuplicate = {}
    duplicateCount = 0
    duplicateUsersSet = set()
    if os.path.exists(path):
        feeds = os.listdir(path)
        for f in feeds:
            readFileDetectDuplicates(path + "/" + f, dictCount, dictDuplicate, printFileNames, performFix)
        if printSummary is True:
            for k in dictCount.keys():
                if int(dictCount[k]) > 1:
                    duplicateCount = duplicateCount + 1
                    if performFix is False:
                        # print out the user IDs with duplicate counts in the dictionary
                        print("[DEBUG] UserId : [ " + k + " ] , occurences: " + str(dictCount[k]))
                    duplicateUsersSet.add(k)
                
            if duplicateCount > 0:
                
                if performFix is False:
                    print("\nIdentified duplicates for : " + dateString + " [ " + str(duplicateCount) + " ]")

                if performFix is True:
                    # if the fix is assumed to be have worked, then run another read only check on the duplicate for this date for
                    # these specific user IDs to make sure that they are set to 1 now.
                    dictCount = {} # reset the dictionary
                    duplicateCount = 0
                    for f in feeds:
                        readFileDetectDuplicates(path + "/" + f, dictCount, {}, False, False)
                    for k in dictCount.keys():
                        if k in duplicateUsersSet:
                            print("[DEBUG] UserId : [ " + k + " ] , occurences: " + str(dictCount[k]))
                            if int(dictCount[k]) > 1:
                                duplicateCount = duplicateCount + 1   

        if duplicateCount > 0:
            return True
        else:
            return False
    else:
        print("[ERROR] " + path + " does not exist")
        return False




"""Identify dates for all feeds for all dates on the file system"""
def identifyDuplicateUserDataAcrossAllDatesOnFileSystem(performFix):
    path = ".././feeds"
    numberOfFeedDirsWithDuplicates = 0
    if (os.path.exists(path)):
        feedDirectories = os.listdir(path)
        for dateStringDir in feedDirectories:
            containsDuplicates = identifyDuplicateUserData(dateStringDir, False, True, performFix)
            if containsDuplicates is True:
                numberOfFeedDirsWithDuplicates = numberOfFeedDirsWithDuplicates + 1
    print("Number of feed directories containing duplicates : " + str(numberOfFeedDirsWithDuplicates))



"""
To identify any corrupt feed files that have incomplete rows of data
"""
def checkCorruptData(dateString):
    feedsPath = ".././feeds/" + dateString
    if os.path.exists(feedsPath):
        feeds = os.listdir(feedsPath)
        for feed in feeds:
            f = open(feedsPath + "/" +feed, "r", encoding="UTF-8")
            lines = f.read().splitlines()
            f.close()
            for line in lines:
                if line == "None":
                    print("[WARN] File : " + feed + " contains 'None'")
                else:
                    fields = line.split("|")
                    if len(fields) < 22:
                        print("[WARN] File : " + feed + " has less than 22 fields [ contains " + str(len(fields)) + "]")
    else:
        print("[" + feedsPath + "] does not exist")


def checkCorruptDataForAllDatesOnFileSystem():
    feedsDirPath = ".././feeds"
    feedsDirs = os.listdir(feedsDirPath)
    for date in feedsDirs:
        checkCorruptData(date)
        
def getBritishUserIdsList():
    print("[INFO] Getting the List with British UserIds")
    dateString = datetime.datetime.now().strftime("%Y-%m-%d")
    userIds = []
    feedsPath = ".././feeds/" + dateString
    if os.path.exists(feedsPath):
        feeds = os.listdir(feedsPath)
        for feed in feeds:
            f = open(feedsPath + "/" +feed, "r", encoding="UTF-8")
            lines = f.read().splitlines()
            f.close()
            for line in lines:
                if line == "None":
                    print("[WARN] File : " + feed + " contains 'None'")
                else:
                    fields = line.split("|")
                    if len(fields) < 22:
                        print("[WARN] File : " + feed + " has less than 22 fields [ contains " + str(len(fields)) + "]")
                        continue
                    if fields[1] == "British":
                        userIds.append(fields[19])
        # now write this file to disk
        file = open("../temp/temp_british_userid_list.txt", "w", encoding="UTF-8")
        for u in userIds:
            file.write(u + "\n")
        file.close()
    else:
        print("[" + feedsPath + "] does not exist")




if len(sys.argv) > 1:
    if sys.argv[1] == "search":
        if len(sys.argv) == 4:
            singleSearch(sys.argv[2], sys.argv[3])
        else:
            singleSearch(sys.argv[2], None)
    elif sys.argv[1] == "historysearch":
        historySearch(sys.argv[2], 100)
    elif sys.argv[1] == "feeds":
        listAllFeedDates()
    elif sys.argv[1] == "feedback-data":
        #arg2 = either a date string (e.g. 2022-07-05) or "now" (for today)
        #arg3 = rating filter ("Positive", "Negative", "FeedbackOnly") or "NOW" (for all ratings)
        #arg4 = userId
        getFeedbackDataForUser(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "master-file":
        generateUserMasterFile()
    elif sys.argv[1] == "duplicates":
        dateString = None
        if len(sys.argv) == 2:
            dateString = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            dateString = sys.argv[2]
        identifyDuplicateUserData(dateString, True, False, False)
    elif sys.argv[1] == "duplicates-fix":
        dateString = None
        if len(sys.argv) == 2:
            dateString = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            dateString = sys.argv[2]
        identifyDuplicateUserData(dateString, True, False, True)
    elif sys.argv[1] == "corrupt-data":
        dateString = None
        if len(sys.argv) == 2:
            dateString = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            dateString = sys.argv[2]
        checkCorruptData(dateString)
    elif sys.argv[1] == "corrupt-data-all":
        checkCorruptDataForAllDatesOnFileSystem()
    elif sys.argv[1] == "duplicates-all":
        identifyDuplicateUserDataAcrossAllDatesOnFileSystem(False)
    elif sys.argv[1] == "duplicates-fix-all":
        identifyDuplicateUserDataAcrossAllDatesOnFileSystem(True)
    elif sys.argv[1] == "get-british-list":
        getBritishUserIdsList()
    else:
        print("\n[ERROR] Unknown operation\n")
