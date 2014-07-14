from ankiemperor.CityObject import CityObject


class City(object):

    def __init__(self, cityInfo):
        self.__cityId = cityInfo['cityID']
        self.name = cityInfo['city']
        self.price = cityInfo['cityPrice']
        self.constructionsNeeded = cityInfo['constructionsNeeded']
        self.__isCapital = cityInfo['isCapital']
        self.cityObjects = []

    def getCityId(self):
        return self.__cityId

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getConstructionsNeeded(self):
        return self.constructionsNeeded

    def isCapital(self):
        return self.__isCapital

    # Return all cityObjects
    def getCityObjects(self):
        return self.cityObjects

    # Return cityObject by objectID
    def getCityObject(self, objectID):
        for cityObject in self.cityObjects:
            if cityObject.objectID == int(objectID):
                return cityObject

    # Return all unbuilt objects
    # inclConstructing: Include the object currently being build
    def getUnbuiltObjects(self, inclConstructing):
        unbuiltObjects = []
        for object in self.cityObjects:
            if object.isUnbuilt() or (inclConstructing and object.isConstructing()):
                unbuiltObjects.append(object)
        return unbuiltObjects

    # Get the number of completed constructions in this city
    def getCompletedObjectsCount(self):
        return (self.getTotalObjectsCount() - len(self.getUnbuiltObjects(True)))

    # Get the number of total constructions in this city
    def getTotalObjectsCount(self):
        return len(self.cityObjects)

    # Add a new cityObject to the city
    def addCityObject(self, cityObjectInfo):
        cityObject = CityObject(cityObjectInfo)
        cityObject.cityName = self.name
        self.cityObjects.append(cityObject)

    # Has the city been unlocked yet?
    def isUnlocked(self):
        return self.price == 0

    def unlock(self):
        self.price = 0

    # Compare cities by city id
    def __eq__(self, other):
        if self.__cityId == other.getCityId():
            return True
        return False
