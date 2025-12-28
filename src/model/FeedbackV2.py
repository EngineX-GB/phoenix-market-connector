class FeedbackV2:

    def __init__(self, id, forUserId, forUserName, byUserId, byUserName, byUserTotalRating, ratingDate, isPositive,
                isNegative, isNeutral, isDisputed, feedback, feedbackResponse, ratingType, userType, userActive):
        self.id = id
        self.forUserId = forUserId
        self.forUserName = forUserName
        self.byUserId = byUserId
        self.byUserName = byUserName
        self.byUserTotalRating = byUserTotalRating
        self.ratingDate = ratingDate
        self.isPositive = isPositive
        self.isNegative = isNegative
        self.isNeutral = isNeutral
        self.isDisputed = isDisputed
        self.feedback = feedback
        self.feedbackResponse = feedbackResponse
        self.ratingType = ratingType
        self.userType = userType
        self.userActive = userActive
        self.delimiter = "|"

    def generateRecord(self):
        return "".join([str(self.id), self.delimiter,
                        str(self.forUserName), self.delimiter,
                        str(self.byUserId), self.delimiter,
                        str(self.byUserName), self.delimiter,
                        str(self.byUserTotalRating), self.delimiter,
                        str(self.ratingDate), self.delimiter,
                        str(self.isPositive), self.delimiter,
                        str(self.isNegative), self.delimiter,
                        str(self.isNeutral), self.delimiter,
                        str(self.isDisputed), self.delimiter,
                        str(self.feedback), self.delimiter,
                        str(self.feedbackResponse), self.delimiter,
                        str(self.ratingType), self.delimiter,
                        str(self.userType), self.delimiter,
                        str(self.userActive)])