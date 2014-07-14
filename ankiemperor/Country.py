from ankiemperor.City import City


class Country(object): 
    # The cached number of all constructions in this country
    totalObjectsCount = None
    __datasetVersion = None

    def __init__(self, name):
        self.__name = name
        self.cities = []

    def getName(self):
        return self.__name

    # Set the dataset version of the current country (for update checks)
    def setDatasetVersion(self, datasetVersion):
        self.__datasetVersion = datasetVersion

    # Get the dataset version of the current country (for update checks)
    def getDatasetVersion(self):
        return self.__datasetVersion

    # Return all cities
    def getCities(self):
        return self.cities

    # Return one city
    def getCity(self, cityName):
        for city in self.cities:
            if city.getName() == cityName:
                return city

    def getCityById(self, cityId):
        for city in self.cities:
            if city.getCityId() == cityId:
                return city

    # Add a new city
    def addCity(self, cityInfo):
        newCity = City(cityInfo)

        if newCity not in self.cities:
            self.cities.append(newCity)

    # Get the number of all unbuilt objects in this country,
    # including the one which is currently being constructed
    def getUnbuiltObjectsCount(self):
        unbuiltObjectsCount = 0

        for city in self.cities:
            unbuiltObjectsCount += len(city.getUnbuiltObjects(True))

        return unbuiltObjectsCount

    # Get the total number of all objects in this country (cached)
    def getTotalObjectsCount(self):
        if self.totalObjectsCount is None:
            self.totalObjectsCount = 0
            for city in self.cities:
                self.totalObjectsCount += len(city.getCityObjects())

        return self.totalObjectsCount

    # Return the total number of constructions already completed in this country
    def getCompletedObjectsCount(self):
        return (self.getTotalObjectsCount() - self.getUnbuiltObjectsCount())

    # Get the percentage of completed constructions in this country (0-100)
    def getCompletedObjectsPercentage(self):
        return (self.getCompletedObjectsCount()*100/self.getTotalObjectsCount())
