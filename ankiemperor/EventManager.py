from anki import sound
from ankiemperor.util import *
from collections import deque


class EventManager(object):

    def __init__(self, ae, options, treasureChest):
        self.ae = ae
        self.__events = deque()
        self.__options = options
        self.__treasureChest = treasureChest

    # Create an event for a finished construction
    def createConstructionEvent(self, finishedObject):
        self.__events.appendleft(ConstructionEvent(self.ae, finishedObject, self.__options))

    def createRankEvent(self, rankDescription):
        self.__events.append(RankEvent(self.ae, rankDescription, self.__options))

    def checkStatsEvent(self, stats):
        eventCreated = False

        if (stats.getCardsAnsweredToday() % 50 == 0) and (0 < stats.getCardsAnsweredToday() <= 250):
            self.__events.append(CardsAnsweredStatsEvent(self.ae, stats.getCardsAnsweredToday(), self.__treasureChest, self.__options))
            eventCreated = True
        if stats.isNewRecord():
            self.__events.append(CardsRecordStatsEvent(self.ae, stats.getCardsAnsweredToday(), self.__treasureChest, self.__options))
            eventCreated = True
        return eventCreated

    #def __checkDeckStudyTime(self):
      #deckStats = mw.deck.getStats()
      # If total deck review time > 1 day (60*60*24 seconds)
      #if (deckStats['gReviewTime'] > 86400):
      #  pass
      #reviewTime = '%s, %s' % (deckStats['gReviewTime'], deckStats['dReviewTime'])

    # Return the next event from the queue
    def getNextEvent(self):
        if self.__events:
            return self.__events.popleft()


# Superclass for all events
class Event(object):

    def __init__(self, ae, options):
        self.ae = ae
        self.__options = options

    def performEventAndGetText(self):
        raise NotImplementedError("Should have implemented this")

    # Sound takes a long time to start
    # Sound cuts out if OK is pressed
    def playMajorEventSound(self):
        if self.ae.getOptions().getOption('soundEnabled'):
            sound.play(getMajorEventSound())


# Event when a construction was finished building
class ConstructionEvent(Event):

    def __init__(self, ae, finishedObject, options):
        super(ConstructionEvent, self).__init__(ae, options)
        self.__finishedObject = finishedObject
        self.ae = ae

    def performEventAndGetText(self):
        self.playMajorEventSound()

        # Show the window if autoOpen is True and the window isn't already open
        if self.ae.isHidden() and self.ae.getOptions().getOption('openOnComplete'):
            self.ae.show()

        txt = '<table cellpadding="2"><tr><td><img src="%s" height=60></td>' % getImagePath(self.__finishedObject.cityName, self.__finishedObject.image)
        txt += '<td><p>Your empire is growing!<br>Your people have completed the following construction:<br><span style="font-size:xx-large; font-weight:bold">%s</span></p></td></tr></table>' % self.__finishedObject.name

        return txt


# Event when a construction was finished building
class RankEvent(Event):

    def __init__(self, ae, rankDescription, options):
        super(RankEvent, self).__init__(ae, options)
        self.__newRank = rankDescription
        self.ae = ae

    def performEventAndGetText(self):
        self.playMajorEventSound()
        txt = '<table cellpadding="2"><tr><td><img src="%s" height=60></td>' % getIcon(RANK_UP_ICON)
        txt += '<td><p>Your empire is flourishing!<br>You have been given a <strong>new title</strong> by your people:</p><p style="font-size:x-large; font-weight:bold">%s</p></td></tr></table>' % self.__newRank

        return txt


# Event when a cool number of cards have been answered
class CardsAnsweredStatsEvent(Event):

    def __init__(self, ae, cardsAnswered, treasureChest, options):
        super(CardsAnsweredStatsEvent, self).__init__(ae, options)
        self.__cardsAnswered = cardsAnswered
        self.__treasureChest = treasureChest
        self.ae = ae

    def performEventAndGetText(self):
        self.__treasureChest._addGold(self.__cardsAnswered/2)
        txt = '<table cellpadding="2"><tr><td><img src="%s" height=60></td>' % getIcon(THUMBS_UP_ICON)
        txt += '<td><p>Great work, you have answered <strong>%s cards</strong> today!<br><strong>%s gold</strong> extra for you, now keep going!</td></tr></table>' % (self.__cardsAnswered, self.__cardsAnswered/2)

        return txt


# Event when a record number of cards have been answered
class CardsRecordStatsEvent(Event):

    def __init__(self, ae, cardsAnswered, treasureChest, options):
        super(CardsRecordStatsEvent, self).__init__(ae, options)
        self.__cardsAnswered = cardsAnswered
        self.__treasureChest = treasureChest
        self.ae = ae

    def performEventAndGetText(self):
        self.__treasureChest._addGold(50)
        txt = '<table cellpadding="2"><tr><td><img src="%s" height=60></td>' % getIcon(THUMBS_UP_ICON)
        txt += '<td><p>New record! You have answered <strong>%s cards</strong> today, more than ever before!<br> You are awesome, <strong>50 gold</strong> extra for you!</td></tr></table>' % (self.__cardsAnswered)

        return txt
