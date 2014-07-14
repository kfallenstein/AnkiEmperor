from ankiemperor.util import *
from datetime import date


class Stats(object):

    def __init__(self, db, eventManager):
        self.__db = db
        self.__enableUndo = True
        self.__eventManager = eventManager
        self.__todayStats = None
        latestStats = self.__db.getStats('latest')
        # If there are not stats in the database, create now
        if latestStats is None:
            self.__createNewStats()
            self.__recordStats = self.__todayStats
        # Else, read from database
        else:
            self.__todayStats = dict(self.__db.getStats('latest'))
            self.__recordStats = dict(self.__db.getStats('record'))
        if (self.__todayStats is None) or (date.today() != self.__todayStats['statsDay']):
            self.__createNewStats()

    def cardAnswered(self, lastQuality):
        if lastQuality > 1:
            self.__enableUndo = True

            # If a new day started, create a new stats entry
            if date.today() != self.__todayStats['statsDay']:
                self.save()
                self.__createNewStats()

            # Increase the cards answered count by 1
            self.__todayStats['cardsAnswered'] += 1

            # If a new event has been created, save
            if self.__eventManager.checkStatsEvent(self):
                self.save()
        else:
            self.__enableUndo = False

        return self.getCardsAnsweredToday()

    def getCardsAnsweredToday(self):
        return self.__todayStats['cardsAnswered']

    def isNewRecord(self):
        # Only if the record has not been achieved today
        if (self.__recordStats is not None) and (date.today() != self.__recordStats['statsDay']) and (self.getCardsAnsweredToday() > self.__recordStats['cardsAnswered']):
            self.__recordStats = self.__todayStats
            return True
        else:
            return False

    def __createNewStats(self):
        self.__todayStats = {}
        self.__todayStats['statsDay'] = date.today()
        self.__todayStats['cardsAnswered'] = 0

    def undo(self):
        if self.__enableUndo:
            self.__todayStats['cardsAnswered'] -= 1

    def save(self):
        self.__db.saveStats(self.__todayStats)
