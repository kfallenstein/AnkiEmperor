class CityObject(object):

    def __init__(self, objectInfo):
        self.objectID = objectInfo['objectID']
        self.name = objectInfo['name']
        self.nameOrig = objectInfo['nameOrig']
        self.cityid = objectInfo['cityid']
        self.price = objectInfo['price']
        self.__rounds = objectInfo['rounds']
        self.__state = objectInfo['state']
        self.desc = objectInfo['desc']
        self.image = objectInfo['image']
        self.link = objectInfo['link']
        self.cityName = ''  # Save the city name for faster access

    def getRemainingRounds(self):
        return self.__state

    def getRounds(self):
        return self.__rounds

    # Start building of the object by inverting the state
    def startBuilding(self):
        self.__state = self.__rounds

    # Advance the building process by one round
    def advanceOneRound(self):
        self.__state = self.__state - 1

    # Has the object not been started building yet?
    def isUnbuilt(self):
        if self.__state is None:
            return True
        return False

    # Has the object been built?
    def isBuilt(self):
        if self.__state == 0:
            return True
        return False

    # Is the object currently being cunstructed
    def isConstructing(self):
        if self.__state > 0:
            return True
        return False

    # Undo one round, but don't exceed initial rounds
    def undoOneRound(self):
        if self.__state < self.__rounds:
            self.__state = self.__state + 1
