import re
import datetime
import json

class PhoenixUtil:

    @staticmethod
    def extractUserId(text):
        res = re.search("userID\\=([0-9]+)",  text)
        return res.group(1)

    @staticmethod
    def checkNodeAndReturnValue(node, type):
        if node is None:
            if type == "integer":
                return 0
            else:
                return "-"
        else:
            if type == "integer" and "-" in node.text:
                return 0
        return node.text

    @staticmethod
    def getTodaysDate():
        return datetime.datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def readHeaderData(jsonFilePath):
        with open(jsonFilePath) as handle:
            return json.loads(handle.read())

    @staticmethod
    def convertHeight(txtHeight):
        heightDictionary = {
            "3'8\"" : "1.15",
            "4'0\"" : "1.22",
            "4'1\"": "1.25",
            "4'2\"": "1.27",
            "4'3\"": "1.30",
            "4'4\"": "1.32",
            "4'5\"": "1.35",
            "4'6\"": "1.37",
            "4'7\"": "1.40",
            "4'8\"": "1.42",
            "4'9\"": "1.45",
            "4'10\"": "1.47",
            "4'11\"": "1.50",
            "5'0\"": "1.52",
            "5'1\"": "1.55",
            "5'2\"": "1.57",
            "5'3\"": "1.60",
            "5'4\"": "1.63",
            "5'5\"": "1.65",
            "5'6\"": "1.68",
            "5'7\"": "1.70",
            "5'8\"": "1.73",
            "5'9\"": "1.75",
            "5'10\"": "1.78",
            "5'11\"": "1.80",
            "6'0\"": "1.83",
            "6'1\"": "1.85",
            "6'2\"": "1.88",
            "6'3\"": "1.91",
            "6'4\"": "1.93",
            "6'5\"": "1.96",
            "6'6\"": "1.98",
            "6'7\"": "2.00",
            "6'8\"": "2.03",
            "6'9\"": "2.06",
            "6'10\"": "2.08",
            "6'11\"": "2.11",
            "7'0\"": "2.13"
        }
        return heightDictionary.get(txtHeight)