from ankiemperor.util import *


class Ranks(object):

    def __init__(self, db, eventManager, world):
        self.__goldRanks = db.getRanks(1)
        self.__constructionRanks = db.getRanks(2)
        self.__currentGoldRankPos = 0
        self.__currentConstrRankPos = 0
        self.__eventManager = eventManager
        self.__initialCheck = True
        self.__world = world

    def getRankDescription(self):
        txt = '%s' % self.__getGoldRank()
        txt += ' %s' % self.__getConstructionRank()
        txt += ' of %s' % self.__world.getActiveCountry().getName()

        return txt

    # Get the current gold rank
    def __getGoldRank(self):
        return self.__goldRanks[self.__currentGoldRankPos]['description']

    # Get the current construction rank
    def __getConstructionRank(self):
        return self.__constructionRanks[self.__currentConstrRankPos]['description']

    def updateRank(self, currentGold, constrCompletePercentage, isInitialCheck):
        newGoldRankPos = self.__getRank(self.__goldRanks, currentGold, self.__currentGoldRankPos)
        newConstrRankPos = self.__getRank(self.__constructionRanks, constrCompletePercentage, self.__currentConstrRankPos)

        # If a rank has changed
        if ((newGoldRankPos != self.__currentGoldRankPos) or (newConstrRankPos != self.__currentConstrRankPos)):
            self.__currentGoldRankPos = newGoldRankPos
            self.__currentConstrRankPos = newConstrRankPos

            # Create an event if this is not the initial determination of the rank
            if not isInitialCheck:
                self.__eventManager.createRankEvent(self.getRankDescription())

        self.__currentGoldRankPos = self.__getRank(self.__goldRanks, currentGold, self.__currentGoldRankPos)
        self.__currentConstrRankPos = self.__getRank(self.__constructionRanks, constrCompletePercentage, self.__currentConstrRankPos)

    # Get the current rank
    def __getRank(self, ranks, rankToCheck, currentRankPos):

        # If a new rank is reached, determine the new rank
        while ((currentRankPos < len(ranks)-1) and (rankToCheck >= ranks[currentRankPos+1]['rankLimit'])):
            currentRankPos += 1

        return currentRankPos
