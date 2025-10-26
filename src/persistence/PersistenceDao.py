from persistence.IPersistence import IPersistence
import json

class PersistenceDao(IPersistence):

    def __init__(self, propertyManager):
        self.propertyManager = propertyManager

    def start(self):
        print("[INFO] start() not implemented")

    def save (self, records):
        f = open("test.txt", "w", encoding="utf-8")
        jsonObjects = []
        for rec in records:
            jsonObject = json.dumps(rec.__dict__, ensure_ascii=False)
            jsonObjects.append(jsonObject)
        
        for j in jsonObjects:
            #print(str(j))
            f.write(j)
        f.close()
        print("[INFO] save() not implemented")

    def getOutstandingUserProfiles(self, userProfileUrlList):
         print("[INFO] getOutstandingUserProfiles() not implemented")
         # a hack to get this test the downloading of data
         return userProfileUrlList    

    def updateUserTempDataFile(self, urls):
        print("[INFO] updateUserTempDataFile() not implemented")

    def handleError (self, records):
        print("[INFO] handleError() not implemented")