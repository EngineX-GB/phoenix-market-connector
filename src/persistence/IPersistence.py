import abc

class IPersistence(metaclass=abc.ABCMeta):
   
    @abc.abstractmethod
    def start (self):
        pass

    @abc.abstractmethod
    def save(self, records):
        pass

    @abc.abstractmethod
    def handleError(self, records):
        pass

    @abc.abstractmethod
    def getOutstandingUserProfiles(self, userProfileUrlList):
        pass

    @abc.abstractclassmethod
    def updateUserTempDataFile(urls):
        pass