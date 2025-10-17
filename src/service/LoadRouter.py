from flask import Blueprint
import json
from util.PropertyFileReader import PropertyFileReader
from model.PropertyManager import PropertyManager
from PhoenixMobileConnector import PhoenixMobileConnector
from persistence.PersistenceDao import PersistenceDao

propertyFileReader = PropertyFileReader(".././properties/config.properties")
propertyManager = PropertyManager(propertyFileReader)
persistence = PersistenceDao(propertyManager)
connector = PhoenixMobileConnector(propertyManager, persistence)

appRoute = Blueprint('approute', __name__)

@appRoute.route('/v2/load/region/<region>')
def loadByRegion(region):
    if connector is not None:
        connector.start()
        connector.main(region)
    return "region = " + str(region)


@appRoute.route('/v2/stats')
def getStats():
    statsMap = connector.getNumberOfPagesPerRegion()
    return json.dumps(statsMap)

@appRoute.route('/v2/load/region/all')
def loadAllRegions():
    if connector is not None:
        connector.start()
        for i in range(1,14):
            if i!=13:
                connector.main(str(i))