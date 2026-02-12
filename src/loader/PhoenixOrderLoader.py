import os
import uuid
from datetime import datetime

from model.Order import Order
from model.OrderClientDetail import OrderClientDetail
from model.PropertyManager import PropertyManager
from util.PhoenixUtil import PhoenixUtil


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

    def handle_manual_entry_parameters(self):
        username = input("Enter Username: ")
        location = input("Select Location: ")
        region = input("Region: ")
        rate_1_H = input("Enter rate: ")
        order_client_detail = OrderClientDetail(username, location, region, rate_1_H)
        return order_client_detail

    def execute(self, manual_entry):
        print("Starting Order Loader Console")
        order_client_detail = None
        user_id = input("Enter the user ID: ")
        if manual_entry:
            order_client_detail = self.handle_manual_entry_parameters()
        else:
            try:
                # automate this by looking up the data in today's feed
                matched_record = self.auto_populate_order_details(user_id)
                if matched_record is not None:
                    username = matched_record["username"]
                    location = matched_record["location"]
                    region = matched_record["region"]
                    rate_1_H = matched_record["rate_1h"]
                    order_client_detail = OrderClientDetail(username, location, region, rate_1_H)
                else:
                    order_client_detail = self.handle_manual_entry_parameters()
            except:
                print("[ERROR] An error occurred when trying to auto populate fields. Re-run with --manual flag enter manually")
                return
        duration = input("Enter duration: [1, 1.5, 2...] (1) ") or "1"
        surplus = input("Enter cost of extras/ surplus: (0) ") or "0"
        deductions = input("Enter cost of deductions: (0) ") or "0"
        date_value = input("Enter date [yyyy-MM-dd]: (" + datetime.now().strftime("%Y-%m-%d") + ") ") or datetime.now().strftime("%Y-%m-%d")
        time_value = input("Enter time [HH:mm:ss]: ") or "00:00:00"
        notes_value = input("Additional notes") or "Newly created order"


        print(f"""
        User ID : {user_id},
        Username : {order_client_detail.username}
        Location: {order_client_detail.location},
        Region: {order_client_detail.region},
        Duration: {duration},
        Rate (1H): {order_client_detail.rate_1_H},
        Surplus: {surplus},
        Deductions: {deductions},
        Date : {date_value},
        Time : {time_value},
        """)
        confirm = input("Confirm? [y/n] ")
        if "y" == confirm.lower():
            print("Updating Order Book")
            new_order_id = self.get_last_order_id() + 1
            order_ref = uuid.uuid4()
            price = int(order_client_detail.rate_1_H) + int(surplus) - int(deductions)
            order = Order(new_order_id, str(order_ref), user_id, order_client_detail.username,
                          order_client_detail.location,
                          date_value, time_value,
                          duration,
                          order_client_detail.rate_1_H,
                          deductions,
                          surplus,
                          price,
                          "COMMITTED", notes_value)
            self.update_order_book(order)
        else:
            print("Order Request is rejected")

    ## TODO: Show list of orders with order ref

    ## cancel an order referencing the order ref

    ## When initialising the order loader, do a check to see that all orders are not in a committed state after the
    ## trade date

    ## amend an order

