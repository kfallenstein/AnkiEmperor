from anki.hooks import wrap
from anki.collection import _Collection  # Undo
from anki.decks import DeckManager
from anki.hooks import *
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.webview import AnkiWebView
from aqt.qt import *
from ankiemperor import *


class AnkiEmperor(QDialog):

    def __init__(self):

        # Setup
        self.db = DBConnect()
        self.__treasureChest = TreasureChest(self.db)
        self.__options = Options(self.db)
        self.__eventManager = EventManager(self, self.__options, self.__treasureChest)
        self.__stats = Stats(self.db, self.__eventManager)
        world = World(self.db, self.__options.getOption('activeCountry'))
        self.__buildingAuthority = BuildingAuthority(self, world)
        self.__ranks = Ranks(self.db, self.__eventManager, world)
        self.__ranks.updateRank(self.__treasureChest.getTotalGold(), self.__buildingAuthority.getActiveCountry().getCompletedObjectsPercentage(), True)
        self.__layout = None    # Setup as a property as we must be able to clear it
        self.__view = None  # Keep's track of current view. Useful if we want to update a view, but we're not sure which one
        self.deckSelected = False

        # Setup window
        QDialog.__init__(self, mw, Qt.WindowTitleHint)
        self.setWindowTitle(getPluginName())
        self.resize(300, 800)
        self.command("MainView||main")

        # Wrap Anki methods
        Reviewer._answerCard = wrap(self.answerCard, Reviewer._answerCard)
        _Collection.undo = wrap(_Collection.undo, self.undo)
        DeckManager.select = wrap(DeckManager.select, self.refreshSettings)

        # Add AnkiEmperor to the Anki menu
        action = QAction(getPluginName(), mw)
        mw.connect(action, SIGNAL("triggered()"), self.show)
        mw.form.menuTools.addAction(action)

    # remember how the card was answered: easy, good, ...
    def setQuality(self, quality):
        self.__lastQuality = quality

    # Gets
    def getTreasureChest(self):
        return self.__treasureChest

    def getBuildingAuthority(self):
        return self.__buildingAuthority

    def getRanks(self):
        return self.__ranks

    def getView(self):
        return self.__view

    def getOptions(self):
        return self.__options

    def getEventManager(self):
        return self.__eventManager

    #Sets
    def setView(self, view):
        self.__view = view

    # Show window
    # Make sure AnkiEmperor shows to the right or left of Anki if possible
    def show(self):

        # Can we display it on the right?
        if (QDesktopWidget().width() - mw.pos().x() - mw.width() - self.width() - 50) > 0:
            self.move(mw.pos().x() + mw.width() + 50, mw.pos().y() - 100)

        # Can we display it on the left?
        elif (QDesktopWidget().width() - mw.pos().x() + self.width() + 50) < QDesktopWidget().width():
            self.move(mw.pos().x() - self.width() - 50, mw.pos().y() - 100)

        # Show window
        super(AnkiEmperor, self).show()

    # This hook makes sure that AnkiEmperor shows after Anki has loaded.
    # This lets us show AnkiEmperor in the correct position
    def onProfileLoaded(self):

         # Show window if required.
        if self.__options.getOption('openOnLaunch'):
            self.show()

    # Take gold away if card undone
    def undo(self, _Collection):
        if self.__options.getOption('pluginEnabled'):
            self.__treasureChest.undo()
            self.__buildingAuthority.undo()
            self.__stats.undo()
            self.command("MainView||main")
            self.__buildingAuthority.save()
            self.__stats.save()

    # Update AnkiEmperor when we answer a card
    def answerCard(self, Reviewer, ease):

        if self.__options.getOption('pluginEnabled'):
            self.setQuality(ease)
            cardsAnsweredToday = self.__stats.cardAnswered(self.__lastQuality)
            self.__stats.save()

            # Update the building process
            self.__buildingAuthority.updateBuildingProgress(self.__lastQuality, cardsAnsweredToday)
            self.__buildingAuthority.save()

            # Update rank
            self.__ranks.updateRank(self.__treasureChest.getTotalGold(), self.__buildingAuthority.getActiveCountry().getCompletedObjectsPercentage(), False)

             # Display popup and perform event action whenever a major event has occured
            event = self.__eventManager.getNextEvent()

            if (event):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.NoIcon)
                msg.setWindowTitle(getPluginName())
                msg.setText(event.performEventAndGetText())
                msg.addButton("OK", QMessageBox.AcceptRole)
                msg.exec_()

            # calculate earned gold
            self.__treasureChest.updateGold(Reviewer.card, self.__lastQuality, cardsAnsweredToday, False)
            self.__treasureChest.save()

            # Update the current view to show new gold etc
            self.command("MainView||main")

    # Update the Anki Emperor Window
    def updateWindow(self, html):

        if html is None:
            return False

        # build view
        webview = AnkiWebView()
        webview.stdHtml(html, mw.sharedCSS)
        webview.setLinkHandler(self.links)

        # Clear old layout
        if self.__layout:
            QObjectCleanupHandler().add(self.__layout)

        # build layout
        self.__layout = QVBoxLayout()
        self.__layout.setMargin(0)
        self.__layout.addWidget(webview)

        # Update window
        self.setLayout(self.__layout)
        self.update()

    # Executes commands
    def command(self, commandString):

        # Split command into an object, method and it's arguments
        # command[0] = object
        # command[1] = method
        # command[2+] = arguments
        command = commandString.split('||')

        # Get the arguments, if any and remove non arguments
        arguments = command[:]
        arguments.pop(0)
        arguments.pop(0)

        # Command to access one of AnkiEmperor's objects
        if command[0] == "ae":

            # We have to remove another argument here. The extra "ae" at the begining of the command means more needs to be removed from the arguments list
            arguments.pop(0)

            # Get AnkiEmperor Object
            aeObject = getattr(self, command[1])()

            # Run object's method
            getattr(aeObject, command[2])(*arguments)
        # Command to change the view
        else:

            # Set View (so we can refresh)
            self.__view = commandString

            # Get HTML
            html = getattr(globals()[command[0]](self), command[1])(*arguments)

            # Update window with new view
            self.updateWindow(html)

    # Method to deal with links
    def links(self, link):

        # Do we want to hide the window?
        if link == "hide":
            self.hide()

        # Is it an external link?
        elif link.startswith("http"):
            QDesktopServices.openUrl(QUrl(link))

        # link must be a command to do something
        else:
            self.command(link)

    # Refresh the settings if the deck is changed
    def refreshSettings(self, DeckManager, did):

        if mw.col is not None:
            self.deckSelected = True
            deck = mw.col.decks.current()
            self.__options.readDeckOptions(deck['id'])


        if self.getView() == "SettingsView||settings":
            self.command(self.getView())

        # Show window if autoOpen is enabled
        if self.__options.getOption('autoOpen') and self.isHidden():
            self.show()
