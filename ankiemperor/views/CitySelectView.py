from ankiemperor.util import *
from operator import attrgetter
from aqt.qt import *  # import all of the Qt GUI library


# The building authority is keeping track of all built attractions
class CitySelectView(object):

    def __init__(self, ae):
        self.treasureChest = ae.getTreasureChest()
        self.buildingAuthority = ae.getBuildingAuthority()

    # City selection view: Select a city where to build a new object
    def selection(self):

        country = self.buildingAuthority.getActiveCountry()
        completedConstructions = country.getCompletedObjectsCount()
        html = "<h1>%s - Cities</h1>" % country.getName()
        html += '<table><tr valign="bottom">'
        html += '<td>Current Gold:</td><td>%s <img src="file:///%s"></td></tr>' % (self.treasureChest.getCurrentGold(), getIcon(GOLD_ICON))
        html += '<tr valign="bottom"><td>Constructed:</td><td>%s <img src="file:///%s"></td></tr></table>' % (completedConstructions, getIcon(CONSTR_ICON))
        html += '<h2>Construct</h2>'
        html += '<p>Select a city where to construct:</p>'
        html += ('''
            <style type="text/css">
                table.alternate tr:nth-child(odd)   { background-color:#f3f3f3; }
                table.alternate tr:nth-child(even)    { background-color:#e7e7e7; }
            </style>''')

        unlockhtml = ''
        constructedhtml = ''

        for city in sorted(country.getCities(), key=attrgetter('price')):

            if city.isCapital():
                capitalIcon = '<img src="file:///%s">' % getIcon(STAR_ICON)
            else:
                capitalIcon = ''

            if city.isUnlocked():
                constructedhtml += '<tr><td colspan="3" valign="middle">'
                constructedhtml += '<a href="CitySelectView||construction||%s||%s"><strong style="font-size:x-large;">%s</strong></a>' % (country.getName(), city.getName(), city.getName())
                constructedhtml += '</td><td align="right">'

                if city.getCompletedObjectsCount() == city.getTotalObjectsCount():
                    constructedhtml += '<span style="color:green">%i / %i</span>' % (city.getCompletedObjectsCount(), city.getTotalObjectsCount())
                else:
                    constructedhtml += '%i / %i' % (city.getCompletedObjectsCount(), city.getTotalObjectsCount())
                constructedhtml += '</td></tr>'
            else:
                goldAndConstructionColors = self.__getGoldAndConstructionColor(city, self.treasureChest.getCurrentGold(), completedConstructions)
                unlockhtml += '<tr><td>%s</strong> %s</td>' % (city.getName(), capitalIcon)
                unlockhtml += '<td width="70"><font color="%s">%s</font> <img src="file:///%s"><br />' % (goldAndConstructionColors[1], city.getConstructionsNeeded(), getIcon(CONSTR_ICON))
                unlockhtml += '<font color="%s">%s</font> <img src="file:///%s"></td>' % (goldAndConstructionColors[0], city.getPrice(), getIcon(GOLD_ICON))

                if (city.getPrice() <= self.treasureChest.getCurrentGold() and self.__allCitiesUnlockedIfCapital(country, city) and city.getConstructionsNeeded() <= completedConstructions):
                    unlockhtml += '<td width="30"><a href="CitySelectView||unlockPopup||%s||%s">Unlock</a></td>' % (country.getName(), city.getName())
                else:
                    unlockhtml += '<td width="30"><font color="gray">Unlock</font></td></tr>'

        # Display the constructed table
        html += '<table class="alternate" width="100%" cellspacing="0" cellpadding="3">'
        html += constructedhtml
        html += '</table>'

        # Display the unlock table
        html += '<h2>Unlock</h2>'
        html += '<p>Select a city to unlock:</p>'
        html += '<table width="100%" class="alternate" cellspacing="0" cellpadding="3">'
        html += unlockhtml
        html += '</table><br>'

        # Display the icon legend
        html += self.__getCitySelectionLegend()

        html += '<br><br><a href="MainView||main">&lt;&lt; Back to main view</a>'

        return html

    # Returns the color for the gold and construction text to indicate what is missing
    def __getGoldAndConstructionColor(self, city, currentGold, completedConstructions):
        colors = ['black', 'black']
        if (city.getPrice() > currentGold):
            colors[0] = 'red'

        if (city.getConstructionsNeeded() > completedConstructions):
            colors[1] = 'red'

        return colors

    def __allCitiesUnlockedIfCapital(self, country, city):
        allCitiesUnlocked = True

        if city.isCapital():

            for otherCity in country.getCities():

                # If there is at least one city not unlocked, return false
                if (city is not otherCity) and not otherCity.isUnlocked():
                    allCitiesUnlocked = False
                    break

        return allCitiesUnlocked

    # Returns a legend for all icons
    def __getCitySelectionLegend(self):
        html = '<p>Unlock legend:</p>'
        html += '<table cellspacing="0" cellpadding="5">'
        html += '<tr><td><img src="file:///%s"></td><td>Capital city: All other cities in this country need to be unlocked first.</td></tr>' % getIcon(STAR_ICON)
        html += '<tr><td><img src="file:///%s"></td><td>Required number of completed constructions in this country.</td></tr>' % getIcon(CONSTR_ICON)
        html += '<tr><td><img src="file:///%s"></td><td>Unlock costs in gold.</td></tr></table>' % getIcon(GOLD_ICON)

        return html

    # Confirmation for unlocking a city
    def unlockPopup(self, countryName, cityName):
        msgBox = QMessageBox()
        city = self.buildingAuthority.getCity(countryName, cityName)
        msgBox.setText("Do you want to unlock %s for %s Gold?" % (city.getName(), city.getPrice()))
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Ok)
        choice = msgBox.exec_()

        if choice == QMessageBox.Ok:

            if self.buildingAuthority.unlockCity(city) is False:
                self.constructionView(countryName, cityName)

    # Build view: Display unbuilt objects and option to build them now
    def construction(self, countryName, cityName):

        html = "<!--AnkiEmperor--><h1>%s Constructions</h1>" % cityName
        html += '<p>Current Gold: %s <img src="file:///%s"></p>' % (self.treasureChest.getCurrentGold(), getIcon(GOLD_ICON))
        html += '<p>Select an object to construct in %s:</p>' % cityName
        city = self.buildingAuthority.getCity(countryName, cityName)

        if city.getUnbuiltObjects(False):
            unbuiltCounter = 0
            bgColors = ('#f3f3f3', '#e7e7e7')
            html += '<table width="100%" cellspacing="0" cellpadding="3">'

            for unbuilt in city.getUnbuiltObjects(False):

                # Only the 5 cheapest objects can be built
                if unbuiltCounter < 5:
                    html += '<tr bgcolor="%s">' % bgColors[unbuiltCounter % 2]
                    html += '<td width="60" align="center" rowspan="2"><img src="file:///%s" height="40"></td>' % getImagePath(unbuilt.cityName, unbuilt.image)
                    html += '<td valign="middle" rowspan="2"><a href="%s" %s>%s</a></td>' % (unbuilt.link, getLinkColor(), unbuilt.name)
                    html += '<td width="70" valign="bottom" height="50%%">%s <img src="file:///%s"></td>' % (unbuilt.price, getIcon(GOLD_ICON))
                    html += '<td width="30" valign="middle" rowspan="2">'

                    if unbuilt.price <= self.treasureChest.getCurrentGold():
                        html += '<a href="ae||getBuildingAuthority||buildObject||%s">Build</a>' % unbuilt.objectID
                    else:
                        html += '<font color="gray">Build</font>'

                    html += '</td></tr>'
                    html += '<tr bgcolor="%s"><td valign="bottom" height="50%%">%s <img src="file:///%s"></td></tr>' % (bgColors[unbuiltCounter % 2], unbuilt.getRounds(), getIcon(ROUND_ICON))
                unbuiltCounter += 1
            html += '</table>'

            if unbuiltCounter == 6:
                html += '<p>There are more constructions in %s. Only the five cheapest ones are displayed.</p>' % cityName
        else:
            html += '<p>You have already constructed everything!</p>'

        html += '<br><br><a href="CitySelectView||selection">&lt;&lt; Select another city</a>'

        return html
