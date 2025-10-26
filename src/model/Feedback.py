class Feedback:

    delimiter = "|"
    rating = None
    username = None
    userId = None
    timestamp = None
    purpose = None
    feedbackText = None
    responseText = None

    def __init__(self):
        pass

    def generateRecord(self):
        return str(self.rating) + self.delimiter + str(self.username) + self.delimiter + str(self.userId) + self.delimiter + str(self.timestamp) + self.delimiter + str(self.purpose) + self.delimiter + str(self.feedbackText) + self.delimiter + str(self.responseText)