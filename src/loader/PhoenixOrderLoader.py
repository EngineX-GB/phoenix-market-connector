import os

from src.model.Order import Order
from src.model.PropertyManager import PropertyManager
from src.util.PhoenixUtil import PhoenixUtil


class PhoenixOrderLoader:

    def __init__(self, property_manager: PropertyManager):
        self.property_manager = property_manager

    def get_user_details(self, feed_file, user_id):
        f = open(feed_file)
        lines = f.readlines()
        result = None
        for line in lines:
            fields = line.split("|")
            if fields[19] == user_id:
                result = {
                    "userId" : user_id,
                    "username" : fields[0],
                    "location" : fields[2],
                    "region" : fields[21],
                    "rate_1h" : fields[8]
                }
                break
        f.close()
        return result



    def auto_populate_order_details(self, user_id: str):
        if user_id is not None:
            todays_feed_directory = self.property_manager.getFeedsDirectory() + "/" + PhoenixUtil.getTodaysDate()
            if os.path.exists(todays_feed_directory):
                feed_files = os.listdir(todays_feed_directory)
                for f in feed_files:
                    matched_record = self.get_user_details(todays_feed_directory + "/" + f, user_id)
                    if matched_record is not None:
                        return matched_record
        else:
            raise Exception("User ID cannot be null/ none")

    def get_last_order_id(self):
        order_book_feed = self.property_manager.getStaticDirectory() + "/orderbook.txt" # todo: put orders in a separate order feed directory
        if not os.path.exists(order_book_feed):
            open(order_book_feed, 'w', encoding='utf-8').close()
            return 0
        else:
            f = open(order_book_feed)
            lines = f.readlines()
            id = 0
            for line in lines:
                id = int(line.split("|")[0])
            f.close()
            return id



    def update_order_book(self, order: Order):
        order_book_feed = self.property_manager.getStaticDirectory() + "/orderbook.txt" # todo: put orders in a separate order feed directory
        if not os.path.exists(order_book_feed):
            open(order_book_feed).close()
        f = open(order_book_feed, 'a', encoding='utf-8')
        f.write(order.generate_record() + "\n")
        f.close()

    def execute(self, manual_entry):
        print("Starting Order Loader Console")
        user_id = input("Enter the user ID: ")
        if manual_entry:
            username = input("Enter Username: ")
            location = input("Select Location: ")
            region = input("Region: ")
            rate_1_H = input("Enter rate: ")
        else:
            try:
                # automate this by looking up the data in today's feed
                matched_record = self.auto_populate_order_details(user_id)
                if matched_record is not None:
                    username = matched_record["username"]
                    location = matched_record["location"]
                    region = matched_record["region"]
                    rate_1_H = matched_record["rate_1h"]
                else:
                    raise Exception("No matching user could be found to autopopulate data. Rerun this operation "
                                    "with the --manual flag")
            except:
                print("An error occurred when trying to auto populate fields. Re-run with --manual flag enter manually")
                return
        duration = input("Enter duration: ")
        surplus = input("Enter cost of extras/ surplus: ")
        deductions = input("Enter cost of deductions: ")
        date_value = input("Enter date [yyyy-MM-dd]: ")
        time_value = input("Enter time [HH:mm:ss]: ")


        print(f"""
        User ID : {user_id},
        Username : {username}
        Location: {location},
        Region: {region},
        Duration: {duration},
        Rate (1H): {rate_1_H},
        Surplus: {surplus},
        Deductions: {deductions},
        Date : {date_value},
        Time : {time_value},
        """)
        confirm = input("Confirm? [y/n")
        if "y" == confirm.lower():
            print("Updating Order Book")
            new_order_id = self.get_last_order_id() + 1
            price = int(rate_1_H) + int(surplus) - int(deductions)
            order = Order(new_order_id, user_id, username, location, date_value, time_value, duration, rate_1_H, deductions,
                          surplus, price, "COMMITTED", "")
            self.update_order_book(order)
        else:
            print("Order Request is rejected")
