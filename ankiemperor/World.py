from ankiemperor.Country import Country


class World(object):

    def __init__(self, db, activeCountryName):
        self.countries = []
        self.buildingObject = None
        self.finishedObject = None
        self.__createWorldFromDB(db)
        self.activeCountry = None
        self.setActiveCountry(activeCountryName)
        self.db = db

    # Create the world: Countries, cities and cityObjects
    def __createWorldFromDB(self, db):
        # Create countries and cities
        cities = db.getAllCities()

        for city in cities:
            self.getCountry(city['country'], True).addCity(city)

        # Now set the dataVersion for all countries (for update checks)
        for country in self.getCountries():
            country.setDatasetVersion(db.readData('ds%sVersion' % country.getName()))

        # Create city objects
        objects = db.getAllObjects()

        for object in objects:
            # Add the object to the country and city
            self.getCountry(object['country'], False).getCity(object['city']).addCityObject(object)

            # Check if the object is currently being built
            if object['state'] > 0:
                self.buildingObject = self.getCountry(object['country'], False).getCity(object['city']).getCityObject(object['objectID'])

    # Return a country by name
    def getCountry(self, countryName, createIfNotExists):
        country = None

        # Check if country exists and return
        for existingCountry in self.countries:

            if existingCountry.getName() == countryName:
                country = existingCountry

        # If country doesn't exists yet, create new one
        if country is None and createIfNotExists:
            country = Country(countryName)
            self.countries.append(country)

        return country

    # Return a list of all known countries
    def getCountries(self):
        return self.countries

    # Return the object currently being built
    def getBuildingObject(self):
        return self.buildingObject

    # Unlock a city
    def unlockCity(self, city):
        self.db.unlockCity(city.getCityId())
        city.unlock()

    # An object has been started being built
    def startedBuilding(self, buildingObject):
        self.buildingObject = buildingObject
        self.buildingObject.startBuilding()

    # Build of an object has been finished
    def finishedBuilding(self):
        self.finishedObject = self.buildingObject
        self.buildingObject = None

    def updateBuildingProgress(self, cardsAnsweredToday):

        if self.buildingObject:

            # After more than 100 cards, only advance every second round
            if ((cardsAnsweredToday < 100) or (cardsAnsweredToday % 2 == 0)):
                self.buildingObject.advanceOneRound()

                # Check if the build is finished now
                if self.buildingObject.getRemainingRounds() == 0:
                    self.finishedBuilding()
                    return self.finishedObject

        return None

    # Get the currently active country
    def getActiveCountry(self):
        return self.activeCountry

    # Set the currently active country
    def setActiveCountry(self, countryName):
        self.activeCountry = self.getCountry(countryName, False)

    # Undo a constructing round
    def undo(self):
        if self.buildingObject:
            self.buildingObject.undoOneRound()

    # Save the changed objects to the database
    def save(self):
        if self.finishedObject:
            self.db.updateObject(self.finishedObject)
            self.finishedObject = None
        if self.buildingObject:
            self.db.updateObject(self.buildingObject)
