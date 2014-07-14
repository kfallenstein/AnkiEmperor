from ankiemperor.util import *
from operator import attrgetter
from aqt.qt import *


# The building authority is keeping track of all built attractions
class ProgressView(object):

    def __init__(self, ae):
        self.buildingAuthority = ae.getBuildingAuthority()
        self.__treasureChest = ae.getTreasureChest()

    # Display the progress view for all countries
    def overview(self):

        html = "<!--AnkiEmperor--><h1>%s Progress</h1>" % getPluginName()
        html += '<h2>Gold</h2>'
        html += '<p>Total gold earned: %s <img src="file:///%s"></p>' % (self.__treasureChest.getTotalGold(), getIcon(GOLD_ICON))
        html += '<h2>Constructions</h2>'
        #html += '<p>Click on a country for more information:</p>'
        for country in self.buildingAuthority.getCountries():
            html += '<h3>%s</h3>' % (country.getName())
            html += '<p>You have completed %s of %s constructions.</p>' % (country.getCompletedObjectsCount(), country.getTotalObjectsCount())
            html += self._getProgressBar(country.getCompletedObjectsPercentage())
            html += '<p><a href="ProgressView||countryProgress||%s">Click here</a> for more details.</p>' % country.getName()
        html += '<br /><a href="MainView||main">&lt;&lt; Back to main view</a>'

        return html

    # Display the progress view for all cities in one country
    def countryProgress(self, countryName):

        country = self.buildingAuthority.getCountry(countryName)
        html = "<!--AnkiEmperor--><h1>%s Progress</h1>" % countryName
        html += '<p>Click on a city for more information:</p>'

        for city in country.getCities():
            builtObjectCount = len(city.getCityObjects()) - len(city.getUnbuiltObjects(True))
            html += '<table><tr><td><h3><a href="ProgressView||cityProgress||%s||%s">%s</a>:</h3></td></tr>' % (countryName, city.getName(), city.getName())
            html += '<tr><td>'

            if (len(city.getCityObjects()) > 0):
                html += self._getProgressBar(builtObjectCount*100/len(city.getCityObjects()))
            else:
                html += self._getProgressBar(0)

            html += '</tr></td>'
            html += '<tr><td>You have completed %s of %s constructions.</tr></td></table><br>' % (builtObjectCount, len(city.getCityObjects()))

        html += '<br><a href="ProgressView||overview">&lt;&lt; Back to progress overview</a>'
        html += '<br><a href="MainView||main">&lt;&lt; Back to main view</a>'

        return html

    def cityProgress(self, countryName, cityName):

        #country = self.buildingAuthority.getCountry(countryName)
        city = self.buildingAuthority.getCity(countryName, cityName)
        html = '<!--AnkiEmperor--><h1>%s Constructions</h1>' % city.getName()
        html += '<p>You have completed the following constructions in %s:</p>' % city.getName()
        html += '<table cellspacing="0" cellpadding="3">'
        # Prepare string for unconstructed items
        unbuilthtml = '<p>Not yet constructed:</p>'
        # Iterate over all city objects (sorted by name)
        for object in sorted(city.getCityObjects(), key=attrgetter('name')):
            if object.isBuilt():
                html += '<tr valign="middle"><td width="50" align="center"><img src="file:///%s" height="40"></td>' % getImagePath(object.cityName, object.image)
                html += '<td><a href="%s" %s>%s</a></td></tr>' % (object.link, getLinkColor(), object.name)
            else:
                unbuilthtml += '%s<br>' % (object.name)
        html += '</table><br>'
        html += unbuilthtml

        html += '<p><a href="ProgressView||countryProgress||%s">&lt;&lt; Back to country progress overview</a>' % (countryName)
        html += '<br><a href="MainView||main">&lt;&lt; Back to main view</a></p>'

        return html

    # Returns a progrss bar with the given percent
    # percentComplete must be between 0 and 100
    def _getProgressBar(self, percentComplete):
        (leftString, rightString) = '', ''
        if percentComplete > 15:
            leftString = '%s %%' % percentComplete
        else:
            rightString = '&nbsp;%s %%' % percentComplete

        html = '<table width="200" cellspacing="0" border="1"><tr>'
        html += '<td width="%s" bgcolor="#87CEFA">%s</td><td width="%s" bgcolor="#EEEEEE">%s</td>' % (2*percentComplete, leftString, 200-2*percentComplete, rightString)
        html += '</tr></table>'

        return html
