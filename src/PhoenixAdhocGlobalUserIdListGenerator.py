import os


class PhoenixAdhocGlobalUserIdListGenerator:

    def __init__(self, root_feedback_dir):
        self.root_feedback_dir = root_feedback_dir
        pass

    def create_global_user_id_list(self, user_id_set, global_file_path):
        f = open(global_file_path, 'w', encoding='utf-8')
        for u in user_id_set:
            f.write(u + "\n")
        f.close()

    def execute(self):
        user_id_set = set()
        if not os.path.exists(self.root_feedback_dir):
            print("[ERROR] " + self.root_feedback_dir + " does not exist.")
            return set()
        else:
            root = os.listdir(self.root_feedback_dir)
            for dir in root:
                self.list_feed_files(self.root_feedback_dir + "/" + dir, user_id_set)
            return user_id_set

    def list_feed_files(self, dated_directory, user_id_set):
        files = os.listdir(dated_directory)
        for f in files:
            self.collect_user_ids_from_feed_files(dated_directory + "/" + f, user_id_set)

    def collect_user_ids_from_feed_files(self, feed_file_path, user_id_set: set):
        f = open(feed_file_path, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        for line in lines:
            fields = line.split("|")
            if len(fields) >= 20:
                if len(fields[19]) <= 10:
                    user_id_set.add(fields[19])
                else:
                    print(
                        "[WARN] Line in " + feed_file_path + " contains a userid "
                                                             "that is greater than 10. Value = [" + fields[19] + "]")
            else:
                print("[WARN] Line in " + feed_file_path + " contains less than 20 fields")


if __name__ == "__main__":
    generator = PhoenixAdhocGlobalUserIdListGenerator("C:/Users/Dell/Documents/phoenix-feed-prod/feeds")
    global_user_id_set = generator.execute()
    if len(global_user_id_set) == 0:
        print("[INFO] No items in the list")
    else:
        print("[INFO] Total number of User IDs collected : " + str(len(global_user_id_set)))
        generator.create_global_user_id_list(global_user_id_set, "C:/Users/Dell/Documents/global-userid-list.txt")
