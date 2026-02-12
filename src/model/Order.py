class Order:

    def __init__(self, id, user_id, username, location, date_of_event,
                 time_of_event, duration, rate, deductions, surplus,
                 price, status, notes):
        self.id = id
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
        self.DELIMITER = "|"

    def generate_record(self):
        return (str(self.id) + self.DELIMITER
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
                + self.notes
                )