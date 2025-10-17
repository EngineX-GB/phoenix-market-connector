import typing
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import cloudscraper

class EpgTopicLoader:

    def __init__(self):
        pass

    def extractRating(self, contentSegment) -> str:
        if "negative" in contentSegment:
            return "NEGATIVE"
        elif "positive" in contentSegment:
            return "POSITIVE"
        elif "neutral" in contentSegment:
            return "NEUTRAL"
        else:
            return "OTHER"

    def extractAndProcessTopicDate(self,contentSegment) -> str:
        if "Yesterday" in contentSegment:
            return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        elif "Today" in contentSegment:
            return datetime.now().strftime("%Y-%m-%d")
        else:
            dateString =  re.search("[a-zA-Z]+\\s[0-9]{2}\\,\\s[0-9]{4}", contentSegment).group(0)
            d = datetime.strptime(dateString, '%B %d, %Y')
            return d.strftime('%Y-%m-%d')

    def extractTopicId(self,contentSegment) -> str:
        obj =  re.search("topic=([0-9]+)", contentSegment)
        if obj is not None:
            return obj.group(1)
        else:
            return None

    def getContentFeed(self,url) -> str:
        scraper = cloudscraper.create_scraper()
        req = scraper.get(url)
        if req is not None:
            sourceText = req.text
            return sourceText

    def extractRatingRecords(self, content, serviceProviderId, awUserId) -> typing.List[str]:
        topics = []
        if serviceProviderId is None:
            serviceProviderId = ""
        if awUserId is None:
            awUserId = ""
        soup = BeautifulSoup(content, "html.parser")
        topicTableElement = soup.find("div", {"class" : "topic_table"})
        if topicTableElement is not None:
            tbodyElement = topicTableElement.find("tbody")
            rows = tbodyElement.find_all("tr")
            # go through each row and read through all the columns
            for row in rows:
                recordDictionary = {}
                record = None
                recordDictionary.update({"serviceProviderId" : serviceProviderId})
                recordDictionary.update({"awUserId" : awUserId})
                columns = row.find_all("td")
                for col in columns:
                    res = "icon2" in col.attrs.get("class")
                    if "icon2" in col.attrs.get("class"):
                        # the rating (positive, negative, neutral)
                        result = self.extractRating(col.find("img").attrs.get("src"))
                        recordDictionary.update({"rating" : result})
                    elif "subject" in col.attrs.get("class"):
                        result = col.find("div").find("a").text
                        if col.find("div").find("a").attrs.get("href") is not None:
                            recordDictionary.update({"topicId" : self.extractTopicId(col.find("div").find("a").attrs.get("href"))})
                        recordDictionary.update({"subject" : result})
                    elif "lastpost" in col.attrs.get("class"):
                        # date of post
                        result = col.text
                        recordDictionary.update({"date" : self.extractAndProcessTopicDate(result)})
                if recordDictionary.get("topicId") is not None:
                    record = recordDictionary.get("topicId") + "|" + recordDictionary.get("serviceProviderId") + "|" + recordDictionary.get("awUserId") + "|" + recordDictionary.get("rating") + "|" + recordDictionary.get("subject") + "|" + recordDictionary.get("date")
                    # only add records if the topicId is not None (sometimes there are rows (topics) that are bogus on the ukp page)
                    topics.append(record)
                else:
                    print("[WARN] Identified topic with topicId of NONE. It's excluded")
        return topics