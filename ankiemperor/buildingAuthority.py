class BuildingAuthority(object):

    def __init__(self, ae, world):
        self.world = world
        self.treasureChest = ae.getTreasureChest()
        self.__eventManager = ae.getEventManager()
        self.ae = ae
        self.__currentCity = None
        self.enableUndo = False

    # Return the object currently being build
    def getBuildingObject(self):
        return self.world.getBuildingObject()

    # Start building an object and return that objects data
    def buildObject(self, objectid):

        # buildObject should not be called if already building: Error!
        #if self.getBuildingObject():
        #    raise
        if self.__currentCity and not self.world.getBuildingObject():
            buildObject = self.__currentCity.getCityObject(objectid)

            # Substract the cost of the city from the current gold
            if self.treasureChest.useGold(buildObject.price) is True:
                self.world.startedBuilding(buildObject)
                self.save()

        self.ae.command('MainView||main')

    # Update the building progress.
    # Returns True if a construction is complete
    def updateBuildingProgress(self, lastQuality, cardsAnsweredToday):
      # Only if the last card was not failed, construnctions are updated
        if lastQuality > 1:
            self.enableUndo = True
            finishedObject = self.world.updateBuildingProgress(cardsAnsweredToday)
            if finishedObject:
                self.__eventManager.createConstructionEvent(finishedObject)
                self.save()
                return True
        else:
            self.enableUndo = False

    # Return a list of all countries
    def getCountries(self):
        return self.world.getCountries()

    # Return a country
    def getCountry(self, countryName):
        return self.world.getCountry("Japan", False)

    def getActiveCountry(self):
        return self.world.getActiveCountry()

    # Return a city by country and cityname
    def getCity(self, countryName, cityName):
        self.__currentCity = self.world.getCountry(countryName, False).getCity(cityName)
        return self.__currentCity

    # Unlock a city
    def unlockCity(self, city):
        # Substract the cost of the city from the current gold
        if self.treasureChest.useGold(city.getPrice()) is True:
            self.world.unlockCity(city)
            self.save()
            self.ae.command('CitySelectView||selection')
            return True
        else:
            return False

    def getEventManager(self):
        return self.__eventManager

    def getDatasetVersions(self):
        datasetVersions = {}

        for country in self.getCountries():
            datasetVersions[country.getName()] = country.getDatasetVersion()

        return datasetVersions

    # On undo, decrease the number of rounds
    # Currently, only a single undo is supported
    def undo(self):
        if self.enableUndo:
            self.world.undo()

    # Save the current progress
    def save(self):
        self.treasureChest.save()
        self.world.save()
