from ankiemperor.util import *


# Options
class Options(object):

    def __init__(self, db):
        self.db = db
        self.currentDeck = None
        self.__globalOptions = {}
        self.__deckOptions = {}
        self.initGlobalOptions()

        # Read global options from database
        options = self.db.getOptions(None)

        # Add global options to list
        for option in options:
            self.__globalOptions[option['option']].setValue(option['value'])

    # Set default global options
    def initGlobalOptions(self):
        self.__globalOptions['activeCountry'] = Option('activeCountry', 'Active country', 'The active country in %s. Only one country can be active at a time.' % getPluginName(), 'Japan')
        self.__globalOptions['openOnLaunch'] = BooleanOption('openOnLaunch', 'Open on launch', 'Determines if %s opens automatically when you launch Anki.' % getPluginName(), True)
        self.__globalOptions['openOnComplete'] = BooleanOption('openOnComplete', 'Open on complete', 'Determines if %s opens automatically if it is currently hidden and a construction is completed.' % getPluginName(), True)
        self.__globalOptions['soundEnabled'] = BooleanOption('soundEnabled', 'Sound enabled', 'Determines if a sound is played for major events.', True)

    # Set default deck options
    def initDeckOptions(self):
        self.__deckOptions['pluginEnabled'] = BooleanOption('pluginEnabled', '%s enabled' % getPluginName(), 'Determines if answering cards on this deck will advance the state of %s.' % getPluginName(), True)
        self.__deckOptions['autoOpen'] = BooleanOption('autoOpen', 'AutoOpen enabled', 'Determines if %s opens automatically when loading this deck.' % getPluginName(), True)

    # Read options for the current deck
    def readDeckOptions(self, deckId):
        self.currentDeck = deckId
        self.initDeckOptions()
        options = self.db.getOptions(deckId)

        for option in options:
            self.__deckOptions[option['option']].setValue(option['value'])

    # Change a deck specific option
    def changeDeckOption(self, key, newValue):
        if self.currentDeck:
            self.__deckOptions[key].setValue(newValue)
            self.db.setOption(self.currentDeck, self.__deckOptions[key])

    # Change a global option
    def changeGlobalOption(self, key, newValue):
        self.__globalOptions[key].setValue(newValue)
        self.db.setOption(None, self.__globalOptions[key])

    def getGlobalOptions(self):
        return self.__globalOptions

    def getDeckOptions(self):
        return self.__deckOptions

    # Return the value of an option
    def getOption(self, optionName):
        if optionName in self.__globalOptions:
            return self.__globalOptions[optionName].getValue()
        elif optionName in self.__deckOptions:
            return self.__deckOptions[optionName].getValue()
        else:
            return False


# A single option
class Option(object):

    def __init__(self, name, desc, longDesc, value):
        self.name = name
        self.desc = desc
        self.longDesc = longDesc
        self._value = value

    def getValue(self):
        return self._value

    def setValue(self, newValue):
        self._value = newValue


# A single boolean option (False/True)
class BooleanOption(Option):

    def getValue(self):
        return bool(int(self._value))
