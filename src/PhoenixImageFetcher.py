# image importer for Phoenix Data Service

import os
import urllib.request
import datetime
import hashlib
import requests

class PhoenixImageFetcher:

    def __init__(self, propertyManager):
        self.propertyManager = propertyManager
        self.MEDIA_DIR = propertyManager.getImageDirectory() #"../images"

    def init(self):
        if not os.path.exists(self.MEDIA_DIR):
            os.makedirs(self.MEDIA_DIR)

    # 1. To take a list of user IDS
    # 2. To divide them into a number of sub groups (defined by numberOfGroups parameter)
    # 3. Select the specific sub group of user Ids in that list.
    def splitUserListAndGroup(self, userIdList, numberOfGroups, selectedGroup):
        if len(userIdList) > 0 and len(userIdList) >= numberOfGroups:
            numberOfItemsPerGroup = int(len(userIdList) / numberOfGroups)
            offsetCounter = 0
            listOfGroups = []
            for x in range(0, numberOfGroups):  # groups numbered from 0 (e.g. 3 groups marked as 0, 1, 2)
                group = []
                if x == (numberOfGroups - 1):
                    group = userIdList[offsetCounter:]
                else:
                    group = userIdList[offsetCounter: offsetCounter + numberOfItemsPerGroup]
                listOfGroups.append(group)
                offsetCounter = offsetCounter + numberOfItemsPerGroup
            return listOfGroups[(selectedGroup - 1)]  # selectedGroup will be the index number - starting from 0...n
        else:
            print(
                "[ERROR] Either the number of user Ids in the list is 0 or the number of items in the list are less than the number of required groups")
            return []

    def download_user_image_using_user_master_file(self, user_id, counter, total_user_count, user_list_in_master_file):
        user_directory = self.MEDIA_DIR + "/" + user_id
        if user_id not in user_list_in_master_file:
            #  now check if it is not already in the file system
            if os.path.exists(user_directory) == False:
                os.makedirs(user_directory)
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(self.propertyManager.getImageDomainUrl() + "/ci/f/" + user_id + "_1.jpg",
                                           user_directory + "/" + user_id + "_1.jpg")
                urllib.request.urlretrieve(self.propertyManager.getImageDomainUrl() + "/ci/f/" + user_id + "_2.jpg",
                                           user_directory + "/" + user_id + "_2.jpg")
                urllib.request.urlretrieve(self.propertyManager.getImageDomainUrl() + "/ci/f/" + user_id + "_3.jpg",
                                           user_directory + "/" + user_id + "_3.jpg")
                print("[INFO] Downloaded data for user: " + user_id + " (" + str(counter) + "/" + str(
                    total_user_count) + ")")
            else:
                print("[INFO] Folder " + user_directory + " already exists. Skipping...")
        else:
            print("[INFO] Folder " + user_id + " exists in the master file")

    def download_user_image(self, user_id, counter, total_user_count):
        user_directory = self.MEDIA_DIR + "/" + user_id
        if os.path.exists(user_directory) == False:
            os.makedirs(user_directory)
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(self.propertyManager.getImageDomainUrl() + "/ci/f/" + user_id + "_1.jpg",
                                       user_directory + "/" + user_id + "_1.jpg")
            urllib.request.urlretrieve(self.propertyManager.getImageDomainUrl() + "/ci/f/" + user_id + "_2.jpg",
                                       user_directory + "/" + user_id + "_2.jpg")
            urllib.request.urlretrieve(self.propertyManager.getImageDomainUrl() + "/ci/f/" + user_id + "_3.jpg",
                                       user_directory + "/" + user_id + "_3.jpg")
            print(
                "[INFO] Downloaded data for user: " + user_id + " (" + str(counter) + "/" + str(total_user_count) + ")")
        else:
            print("[INFO] Folder " + user_directory + " already exists. Skipping...")

    # Generic function to get user ids of images that have already been downloaded on the file system
    def get_user_ids_of_downloaded_images(self):
        imagesDirectory = self.propertyManager.getImageDirectory() #"../images"
        if os.path.exists(imagesDirectory):
            userDirectories = os.listdir(imagesDirectory)
            return userDirectories
        else:
            return []

    def get_user_id_folders_with_zero_images(self):
        imagesDirectory = self.propertyManager.getImageDirectory() #"../images"
        emptyFoldersList = []
        userIds = self.get_user_ids_of_downloaded_images()
        for userId in userIds:
            files = os.listdir(imagesDirectory + "/" + userId)
            if len(files) == 0:
                emptyFoldersList.append(userId)
        return emptyFoldersList

    def delete_empty_image_folders(self):
        imagesDirectory = self.propertyManager.getImageDirectory() #"../images"
        emptyFolders = self.get_user_id_folders_with_zero_images()
        if len(emptyFolders) > 0:
            print("[INFO] Deleting " + str(len(emptyFolders)) + " empty folder(s)")
            # delete the folders:
            for f in emptyFolders:
                os.rmdir(imagesDirectory + "/" + f)

    # find the specific user ids that don't have images on the file system (using the temp file) that must
    # be downloaded
    def get_user_ids_required_for_image_data(self, dateString):
        downloaded_user_ids = self.get_user_ids_of_downloaded_images()
        temp_user_ids = self.get_user_ids(dateString)
        # do a diff here and return the number of user ids that need to have images downloaded for the specified date
        return list(set(temp_user_ids) - set(downloaded_user_ids))

    # new function added: 2025-07-27
    # to fetch new image data compared to what has already been previously saved.

    def get_updated_image_data(self, user_id):
        user_directory = self.MEDIA_DIR + "/" + user_id
        highest_file_counter = 0
        if os.path.exists(user_directory) == True:
            # check the files that exist and get their hashes
            file_hashes = []
            # Loop through each file in the directory
            for filename in os.listdir(user_directory):
                number = filename.split('_')[1].split('.')[0]
                if int(number) > highest_file_counter:
                    highest_file_counter = int(number)
                filepath = os.path.join(user_directory, filename)
                if os.path.isfile(filepath):
                    with open(filepath, "rb") as f:
                        file_contents = f.read()
                        file_hash = hashlib.sha256(file_contents).hexdigest()
                        file_hashes.append(file_hash)

            # fetch the new files that exist on the server for the user id
            headers = {"User-agent": "Mozilla/5.0"}
            for i in range(1, 4):
                url = self.propertyManager.getImageDomainUrl + "/ci/f/" + user_id + "_" + str(i) + ".jpg"
                print("[DEBUG] Check file on server to see if hash matches with stored hashes [" + url + "]")
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Throws an error if the request failed

                file_contents = response.content
                file_hash = hashlib.sha256(file_contents).hexdigest()
                if file_hash in file_hashes:
                    print("[DEBUG] File hash [ " + user_id + "_" + str(
                        i) + ".jpg ] matches with stored hash. Skipping...")
                else:
                    print("[DEBUG] File hash does not match with stored hash. It's a new file [" + url + "]")
                    # download the file with a new filecounter appended at the end of the filename
                    highest_file_counter = highest_file_counter + 1
                    new_file_name = user_id + "_" + str(highest_file_counter) + ".jpg"
                    print("[DEBUG] Downloading file : " + new_file_name)
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(self.propertyManager.getImageDomainUrl() + "/ci/f/" + user_id + "_" + str(i) + ".jpg",
                                               user_directory + "/" + new_file_name)
        else:
            print("[INFO] Folder " + user_directory + " does not exist. Run command to download new image data.")

    # reads the temp file to get the list of downloaded user data so far
    def get_user_ids(self, dateString):
        userIds = []
        temp_filename = None
        if dateString == None:
            temp_filename = self.propertyManager.getTempDirectory() + "/temp_userlist_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt"
        else:
            temp_filename = self.propertyManager.getTempDirectory() + "/temp_userlist_" + dateString + ".txt"
        # (for testing purposes only) temp_filename = ".././temp/temp_userlist_2022-01-23.txt"

        file = open(temp_filename, "r", encoding="utf-8")
        lines = file.read().splitlines()
        for l in lines:
            userId = l.split("=")[1]
            userIds.append(userId)
        file.close()
        return userIds

    # Read the master file and return the records from the master file
    def readFromMasterFile(self):
        masterFile = self.propertyManager.getTempDirectory + "/temp_image_master_file.txt" # TODO: here we reference ../temp, but most reference .././temp
        if os.path.exists(masterFile):
            file = open(masterFile, "r", encoding="UTF-8")
            userIds = file.read().splitlines()
            file.close()
        return userIds

    # Run this script using 3 modes
    # 1. standard  - download image data that does not exist on the file system
    # 2. custom    - download image data for a specific user id that does not exist in the system
    # 3. master-file    download image data that does not exist in both the master file and the file system

    def main(self, argList : list[str]):
        self.init()

        dateString = None
        if len(argList) > 1:
            if argList[0] == "standard" or argList[0] == "verify" or argList[0] == "advanced":
                dateString = argList[1]
            else:
                dateString = None  # i.e. if sys.argv[1] is 'custom', then the next parameter is a user ID, not a date. So set the date as None

        print("[DEBUG] Date String: [" + str(dateString) + "]")

        if argList[0] == "standard":
            useridlist = self.get_user_ids(dateString)
            if len(useridlist) > 0:
                counter = 1
                # run the operation here
                print("[INFO] Client data records in temp file = " + str(len(useridlist)))
                for userId in useridlist:
                    self.download_user_image(userId, counter, len(useridlist))
                    counter = counter + 1
            else:
                print("[INFO] There is nothing here to download")

        elif argList[0] == "verify":
            required_user_ids = self.get_user_ids_required_for_image_data(dateString)
            print("[INFO] Verify image data against users profiles as of " + str(
                datetime.datetime.now().strftime("%Y-%m-%d") if dateString is None else dateString))
            print("[INFO] Number of user (images) to download: = " + str(len(required_user_ids)))

        elif argList[0] == "verify-empty-folders":
            empty_user_folders = self.get_user_id_folders_with_zero_images()
            for e in empty_user_folders:
                print("[INFO] userId : " + e)
            print("[INFO] Number of empty user folders: = " + str(len(empty_user_folders)))

        elif argList[0] == "delete-empty-folders":
            self.delete_empty_image_folders()
            empty_user_folders = self.get_user_id_folders_with_zero_images()
            print("[INFO] Number of empty user folders: = " + str(len(empty_user_folders)))

        elif argList[0] == "advanced":
            required_user_ids = self.get_user_ids_required_for_image_data(dateString)
            print("[INFO] Verify image data against users profiles as of " + str(
                datetime.datetime.now().strftime("%Y-%m-%d") if dateString is None else dateString))
            print("[INFO] Number of user (images) to download: = " + str(len(required_user_ids)))
            if len(required_user_ids) > 0:
                counter = 1
                # trigger the download of images
                for userId in required_user_ids:
                    self.download_user_image(userId, counter, len(required_user_ids))
                    counter = counter + 1
            else:
                print("[WARN] No images to download for new users")

        elif argList[0] == "master-file":
            useridlist = self.get_user_ids(dateString)
            # perform the custom logic here
            userIdsFromMasterFile = self.readFromMasterFile()
            if len(useridlist) > 0:
                counter = 1
                # run the operation here
                print("[INFO] Client data records in temp file = " + str(len(useridlist)))
                for userId in useridlist:
                    self.download_user_image_using_user_master_file(userId, counter, len(useridlist),
                                                                    userIdsFromMasterFile)
                    counter = counter + 1

        elif argList[0] == "custom":
            # perform the custom logic here
            useridlist = []
            useridlist.append(argList[1])
            self.download_user_image(argList[1], 1, len(useridlist))

        elif argList[0] == "subgroup":
            # splits user id list into sub groups and downloads image data for a selected sub group of user ids
            # note that this can only refer to user ids from TODAY'S user list (in today's temp client file)
            required_user_ids = self.get_user_ids_required_for_image_data(dateString)
            subgroupList = self.splitUserListAndGroup(required_user_ids, int(argList[1]), int(argList[2]))
            counter = 1
            print("[INFO] Selected subgroup : " + (argList[2]))
            print("[INFO] Number of user IDs in selected subgroup: " + str(len(subgroupList)))
            for userId in subgroupList:
                self.download_user_image(userId, counter, len(subgroupList))
                counter = counter + 1

        elif argList[0] == "update":
            # perform the custom logic here
            userId = argList[1]
            self.get_updated_image_data(userId)

        elif argList[0] == "update-british-data":
            userIds = []
            file = open(self.propertyManager.getTempDirectory() + "/temp_british_userid_list.txt", "r", encoding="utf-8")
            lines = file.read().splitlines()
            print("[INFO] Fetching " + str(len(lines)) + " userIds from temp file")
            for userId in lines:
                userIds.append(userId)
            file.close()
            print("[INFO] Getting ready to fetch new image data based off the list")
            totalUKUsers = len(userIds)
            arbitraryUserCounter = 0
            for id in userIds:
                arbitraryUserCounter = arbitraryUserCounter + 1
                print("[INFO] Examining user Id [" + id + "] (" + str(arbitraryUserCounter) + "/" + str(
                    totalUKUsers) + ")")
                self.get_updated_image_data(id)


        else:
            print("[ERROR] unknown flag.")
