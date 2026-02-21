import os
import shutil
import sys


# Script: ImageFileHelper.py
# An adhoc script to copy specific user files to a temporary location that can be extracted later.
#
# Usage: python ImageFileHelper.py --copy           to copy the media data defined in the uk-userid-list from src to dest
#        python ImageFileHelper.py --delete         to delete the media data at the source, using the user ids from the
#                                                   uk-userid-list
#
# 2026-02-14: This is yet to be tested properly before use.
# 2026-02-21: A global list of UK user Ids are required, not the typical global userid list.

class ImageFileHelper:

    def __init__(self):
        pass

    def copy_image_data(self, user_id_set, src_image_directory, dest_image_directory):
        if not os.path.exists(src_image_directory):
            print(f"[ERROR] {src_image_directory} does not exist")
        if not os.path.exists(dest_image_directory):
            os.makedirs(dest_image_directory, exist_ok=True)
        for user_id in user_id_set:
            source_user_folder = f"{src_image_directory}/{user_id}"
            destination_user_folder = f"{dest_image_directory}/{user_id}"
            if not os.path.exists(source_user_folder):
                #print(f"[WARN] Directory {source_user_folder} does not exist")
                pass
            else:
                # copy the directory and it's contents into the new folder
                print(f"[INFO] Copying {source_user_folder} -> {destination_user_folder} ")
                shutil.copytree(source_user_folder, destination_user_folder, dirs_exist_ok=True)

    def delete_image_data(self, user_id_set, image_directory):
        if not os.path.exists(image_directory):
            print(f"[ERROR] {image_directory} does not exist")
        for user_id in user_id_set:
            user_folder = f"{image_directory}/{user_id}"
            if not os.path.exists(user_folder):
                # print(f"[ERROR] Directory {user_folder} does not exist")
                pass
            else:
                # copy the directory and it's contents into the new folder
                print(f"[INFO] Deleting {user_folder}")
                shutil.rmtree(user_folder)

    def read_user_id_list(self, filepath: str):
        if not os.path.exists(filepath):
            print(f"[ERROR] {filepath} does not exist")
            return set()
        else:
            f = open(filepath, 'r', encoding='utf-8')
            user_ids = f.readlines()
            f.close()
            return set(user_ids)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_file_helper = ImageFileHelper()
        user_id_set = image_file_helper.read_user_id_list("/data/data/com.termux/files/home/storage/dcim/phoenix-market-connector/app-data/static/global-userid-list.txt")
        user_id_set = [line.strip() for line in user_id_set]
        if len(user_id_set) == 0:
            print("[WARN] List is empty. Exiting")
            exit(0)
        if sys.argv[1] == "--copy":
            image_file_helper.copy_image_data(user_id_set, "/data/data/com.termux/files/home/storage/dcim/phoenix/images",
                                              "/data/data/com.termux/files/home/storage/dcim/phoenix-market-connector/app-data/migration/images")
            print("[INFO] Copying completed.")
        if sys.argv[1] == "--delete":
            image_file_helper.delete_image_data(user_id_set, "/data/data/com.termux/files/home/storage/dcim/phoenix/images")
            print("[INFO] Deletion completed.")
    else:
        print("[ERROR] Script must have at least one argument.")
