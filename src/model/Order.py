class Order:

    def __init__(self, id, order_ref, user_id, username, location, date_of_event,
                 time_of_event, duration, rate, deductions, surplus,
                 price, status, notes, timestamp):
        self.id = id
        self.order_ref = order_ref
        self.user_id = user_id
        self.username = username
        self.location = location
        self.date_of_event = date_of_event
        self.time_of_event = time_of_event
        self.duration = duration
        self.rate = rate
        self.deductions = deductions
        self.surplus = surplus
        self.price = price
        self.status = status
        self.notes = notes
        self.timestamp = timestamp
        self.DELIMITER = "|"

    def get_order_ref(self):
        return self.order_ref

    def get_status(self):
        return self.status

    def get_user_id(self):
        return self.user_id

    def get_username(self):
        return self.username

    def get_date_of_event(self):
        return self.date_of_event

    def set_id(self, id):
        self.id = id

    def set_status(self, status):
        self.status = status

    def set_notes(self, notes):
        self.notes = notes

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def generate_record(self):
        return (str(self.id) + self.DELIMITER
                + self.order_ref + self.DELIMITER
                + self.user_id + self.DELIMITER
                + self.username + self.DELIMITER
                + self.location + self.DELIMITER
                + self.date_of_event + self.DELIMITER
                + self.time_of_event + self.DELIMITER
                + self.duration + self.DELIMITER
                + self.rate + self.DELIMITER
                + self.deductions + self.DELIMITER
                + self.surplus + self.DELIMITER
                + str(self.price) + self.DELIMITER
                + self.status + self.DELIMITER
                + self.notes + self.DELIMITER
                + self.timestamp
                )