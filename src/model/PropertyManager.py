class PropertyManager:

    def __init__(self, propertyFileReader):
        self.providerUrl = propertyFileReader.get("provider.url")
        self.apiProviderUrl = propertyFileReader.get("api.provider.url")
        self.tsApiProviderUrl = propertyFileReader.get("ts.api.provider.url")
        self.requestPayload = propertyFileReader.get("request.payload")
        self.requestPayloadNext = propertyFileReader.get("request.payload.next")
        self.feedsDirectory = propertyFileReader.get("feeds.directory")
        self.tempDirectory = propertyFileReader.get("temp.directory")
        self.headersJsonFilePath = propertyFileReader.get("headers.json.file.path")
        self.apiHeadersJsonFilePath = propertyFileReader.get("api.headers.json.file.path")
        self.imageDirectory = propertyFileReader.get("image.directory")
        self.imageDomainUrl = propertyFileReader.get("image.domain.url")
        self.ukpUserProfileUrl = propertyFileReader.get("ukp.user.profile.url")
        self.staticDirectory = propertyFileReader.get("static.directory")
        self.reportsDirectory = propertyFileReader.get("reports.directory")
        self.feedsFeedbackDirectory = propertyFileReader.get("feeds.feedback.directory")
        self.feedsFeedbackV2Directory = propertyFileReader.get("feeds.feedback.v2.directory")
        self.feedsServiceReportsV2Directory = propertyFileReader.get("feeds.service.reports.v2.directory")
        self.feedsFeedbackEpgDirectory = propertyFileReader.get("feeds.feedback.epg.directory")
        self.ingestionServiceEndpoint = propertyFileReader.get("ingestion.service.endpoint")
        self.apiCred = propertyFileReader.get("api.cred")

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

    def getFeedsFeedbackV2Directory(self):
        return self.feedsFeedbackV2Directory

    def getFeedsServiceReportsV2Directory(self):
        return self.feedsServiceReportsV2Directory

    def getFeedsFeedbackEpgDirectory(self):
        return self.feedsFeedbackEpgDirectory

    def getIngestionServiceEndpoint(self):
        return self.ingestionServiceEndpoint

    def getApiProviderUrl(self):
        return self.apiProviderUrl

    def getTsApiProviderUrl(self):
        return self.tsApiProviderUrl

    def getApiCred(self):
        return self.apiCred

    def getApiHeadersJsonPath(self):
        return self.apiHeadersJsonFilePath
