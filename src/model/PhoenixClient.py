class PhoenixClient:

    delimiter = "|"

    userName = None
    age = None
    location = None
    region = None
    gender = None
    nationality = None
    rate15Min = None
    rate30Min = None
    rate45Min = None
    rate1Hour = None
    rate1HalfHour = None
    rate2Hour = None
    rate2HalfHour = None
    rate3Hour = None
    rate3HalfHour = None
    rate4Hour = None
    rateOvernight = None
    refreshTime = None
    userId = None
    urlPage = None
    rating = None
    memberSince = None
    height=None
    dressSize=None
    eyeColour = None
    hairColour = None
    telephone = None
    imageAvailable = 0
    refreshTime=0
    verified = False
    preferenceList = "[]"
    email = None
    ethnicity=None

    def __init__(self):
        pass


    def generateRecord(self):
        return str(self.userName) + self.delimiter + str(self.nationality) + self.delimiter + str(self.location) + self.delimiter + str(self.rating) + self.delimiter + str(self.age) + self.delimiter  + str(self.rate15Min) + self.delimiter + str(self.rate30Min) + self.delimiter + str(self.rate45Min) + self.delimiter + str(self.rate1Hour) + self.delimiter + str(self.rate1HalfHour) + self.delimiter + str(self.rate2Hour) + self.delimiter + str(self.rate2HalfHour) + self.delimiter + str(self.rate3Hour) + self.delimiter + str(self.rate3HalfHour) + self.delimiter + str(self.rate4Hour) + self.delimiter + str(self.rateOvernight) + self.delimiter + str(self.telephone) + self.delimiter + str(self.urlPage) + self.delimiter + str(self.refreshTime) + self.delimiter + str(self.userId) + self.delimiter + str(self.imageAvailable) + self.delimiter + str(self.region) + self.delimiter + str(self.gender) + self.delimiter + str(self.memberSince) + self.delimiter + str(self.height) + self.delimiter + str(self.dressSize) + self.delimiter + str(self.hairColour) + self.delimiter + str(self.eyeColour)+ self.delimiter + str(self.verified) + self.delimiter + str(self.email) + self.delimiter + str(self.preferenceList) + self.delimiter + str(self.ethnicity)