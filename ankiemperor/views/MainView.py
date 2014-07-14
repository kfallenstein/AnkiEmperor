from aqt.qt import *
from ankiemperor.util import *
from ankiemperor.views.ProgressView import ProgressView
from ankiemperor.EventManager import *


class MainView(object):

    def __init__(self, ae):
        self.deckSelected = ae.deckSelected
        self.progressView = ProgressView(ae)
        self.treasureChest = ae.getTreasureChest()
        self.__ranks = ae.getRanks()
        self.buildingAuthority = ae.getBuildingAuthority()
        self.options = ae.getOptions()

    def main(self):

        html = "%s" % getLogo()
        html += """
        <h2>Status</h2>"""

        html += 'Rank: %s <br />' % self.__ranks.getRankDescription()
        html += 'Gold: %s <img src="file:///%s">' % (self.treasureChest.getCurrentGold(), getIcon(GOLD_ICON))

        if self.treasureChest.checkGoldFade() is not None:
            html += """<script>
                        opacity = 100;
                        interval = setInterval(function(){
                            opacity--;
                            document.getElementById('goldFade').style.opacity = opacity/100;
                        }, 1);

                        if (opacity === 0)
                            clearInterval(interval)

                    </script>"""
            html += '<span id="goldFade" style="color: green"> +%s</span>' % self.treasureChest.getGoldFade()

        html += '<br /><h2>Constructing</h2>'
        buildingObject = self.buildingAuthority.getBuildingObject()

        if buildingObject:
            html += '<p align="center"><strong style="font-size:xx-large;">%s</strong><br>(<a href="%s" %s>%s</a>)</p>' % (buildingObject.nameOrig, buildingObject.link, getLinkColor(), buildingObject.name)
            html += '<p align="center"><img src="file:///%s"></p>' % getImagePath(buildingObject.cityName, buildingObject.image)
            html += '<p align="center">%s</p>' % buildingObject.desc
            html += 'Current city: %s' % buildingObject.cityName
            html += '<p style="font-size:large;">Remaining rounds: <strong>%s </strong><img src="file:///%s"></p>' % (buildingObject.getRemainingRounds(), getIcon(ROUND_ICON))
            html += self.progressView._getProgressBar((buildingObject.getRounds()-buildingObject.getRemainingRounds())*100/buildingObject.getRounds())
            html += '<br>'
        else:
            html += '<p>No construction in progress.</p>'
            html += '<p style="font-size:x-large;"><a href="CitySelectView||selection">Start a construction</a></p>'

        html += """
        <h2>Options</h2>
        <a href="ProgressView||overview">Progress</a><br />
        <br />
        <a href="SettingsView||settings">Settings</a><br />
        <br />
        <a href="HelpView||help">Help</a><br />
        <br />
        <a href="hide">Hide</a><br />
        """

        if not self.options.getOption('pluginEnabled') and self.deckSelected:
            html += "<p>AnkiEmperor is disabled on this deck.</p>"

        return html
