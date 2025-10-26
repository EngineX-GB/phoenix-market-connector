class PropertyManager:

    def __init__(self, propertyFileReader):
        self.providerUrl = propertyFileReader.get("provider.url")
        self.requestPayload = propertyFileReader.get("request.payload")
        self.requestPayloadNext = propertyFileReader.get("request.payload.next")
        self.feedsDirectory = propertyFileReader.get("feeds.directory")
        self.tempDirectory = propertyFileReader.get("temp.directory")
        self.headersJsonFilePath = propertyFileReader.get("headers.json.file.path")
        self.imageDirectory = propertyFileReader.get("image.directory")
        self.imageDomainUrl = propertyFileReader.get("image.domain.url")
        self.ukpUserProfileUrl = propertyFileReader.get("ukp.user.profile.url")
        self.staticDirectory = propertyFileReader.get("static.directory")
        self.reportsDirectory = propertyFileReader.get("reports.directory")
        self.feedsFeedbackDirectory = propertyFileReader.get("feeds.feedback.directory")
        self.feedsFeedbackEpgDirectory = propertyFileReader.get("feeds.feedback.epg.directory")
        
    def getProviderUrl(self):
        return self.providerUrl
    
    def getRequestPayload(self):
        return self.requestPayload

    def getRequestPayloadNext(self):
        return self.requestPayloadNext

    def getFeedsDirectory(self):
        return self.feedsDirectory

    def getTempDirectory(self):
        return self.tempDirectory

    def getHeadersJsonFilePath(self):
        return self.headersJsonFilePath

    def getImageDirectory(self):
        return self.imageDirectory

    def getImageDomainUrl(self):
        return self.imageDomainUrl

    def getUkpUserProfileUrl(self):
        return self.ukpUserProfileUrl

    def getReportsDirectory(self):
        return self.reportsDirectory

    def getStaticDirectory(self):
        return self.staticDirectory

    def getFeedsFeedbackDirectory(self):
        return self.feedsFeedbackDirectory

    def getFeedsFeedbackEpgDirectory(self):
        return self.feedsFeedbackEpgDirectory