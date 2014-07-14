from ankiemperor.util import *
from array import array


class TreasureChest(object):

    NEW_CARD_GOLD = 12
    CARD_GOLD = 2

    def __init__(self, db):
        self.db = db
        self.currentGold = int(self.db.readData('currentGold'))
        self.__totalGold = int(self.db.readData('totalGold'))
        # Amount of gold gained, used for undo functionality
        self.undoGold = array('i')
        self.goldFade = None
        self.newGold = 0

    def getCurrentGold(self):
        return self.currentGold

    def checkGoldFade(self):
        return self.goldFade

    def getGoldFade(self):
        gold = self.goldFade
        self.goldFade = None
        return gold

    # addGold stores gold to add on next card answered
    def _addGold(self, gold):
        self.newGold += gold

    # Use gold and substract from current gold
    def useGold(self, gold):
        if gold <= self.currentGold:
            self.currentGold -= gold
            return True
        else:
            return False

    def getTotalGold(self):
        return self.__totalGold

    # This makes sure the gold and events show at the right time
    def updateGold(self, card, lastQuality, cardsAnsweredToday, undo=True):
        # calculate bonus based on maturity
        if (card.queue == 0):
            self.newGold += self.NEW_CARD_GOLD
        else:
            self.newGold += self.CARD_GOLD

        # calculate bonus based on ease
        bonus = 0

        if (1 < lastQuality <= 4):
            bonus = lastQuality

        # Sadly I can't find anything that shows how many times a card has been answred successivly correct
        # Multiplier if card have been ansered successively correct
        # multiplier = card.what?/2
        # if (multiplier < 1):
        #     multiplier = 1
        # elif (multiplier > 4):
        #     multiplier = 4
        # bonus = bonus * multiplier

        bonus *= 2  # Compensate for no multiplier

        # Reduce gold after many cards a day
        if cardsAnsweredToday > 200:
            bonus = bonus * 0.25
        elif cardsAnsweredToday > 100:
            bonus = bonus * 0.5
        elif cardsAnsweredToday > 50:
            bonus = bonus * 0.75

        self.newGold += int(round(bonus))

        self.undoGold.append(self.newGold)

        # Update gold
        self.currentGold += self.newGold
        self.__totalGold += self.newGold

        # The gold fader (+5, +3 etc)
        self.goldFade = self.newGold

        # Set newGold back to 0
        self.newGold = 0

        #deckstats = anki.stats.DeckStats(mw.deck)
        #cardcount1day = deckstats.getRepsDone(-1, 0)

    # On undo, substract the gold from the last round
    def undo(self):
        self.currentGold += (self.undoGold[-1] * -1)
        self.undoGold.pop()

        # If we have gone through all the undos, just take 2 away for the rest
        if len(self.undoGold) < 1:
            self.undoGold.append(2)

        # If there are more than 40 undos, start deleting them.
        if len(self.undoGold) > 40:
            self.undoGold.pop(0)

    # Save progress to database
    def save(self):
        self.db.writeData('currentGold', self.currentGold)
        self.db.writeData('totalGold', self.__totalGold)
