class PropertyFileReader:

    properties = {}
        
    def __init__(self, propertiesFilePath):
        f = open(propertiesFilePath, "r", encoding="UTF-8")
        lines = f.read().splitlines()
        for line in lines:
            property = line.split("=", 1)
            key = property[0]
            value = property[1]
            self.properties[key] = value

    def get(self, key):
        return self.properties[key]