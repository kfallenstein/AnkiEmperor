import codecs
import os.path
import sqlite3
from ankiemperor.util import *


class DBConnect(object):

    def __init__(self):
        doesDbExist = True
        self.db = os.path.join(getAWFolder(), 'ankiemperor.db')

        # If there is no db file, it has to be created later
        if not os.path.isfile(self.db):
            doesDbExist = False

        # Connect to the database
        self.conn = sqlite3.connect(self.db, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

        # If there is no db file or the version has changed, create the database now
        if not doesDbExist or (self.readData('aeVersion') != '1.1.0'):
            self.__createDatabase()

        # Update the database if necessary
        self.__updateDB()

    # Load from database
    def getAllObjects(self):
        self.c.execute("select o.*, c.* from objects o, cities c where o.cityid = c.cityID order by o.price")
        result = self.c.fetchall()
        return result

    # Read general data from database
    def readData(self, name):
        self.c.execute("select value from user where name = ?", [name])
        result = self.c.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    # Write general data to database
    def writeData(self, name, value):
        self.c.execute("update user set value = ? where name = ?", (value, name))
        self.conn.commit()

    # Update an object in the database
    def updateObject(self, object):
        self.c.execute("update objects set state = ? where objectid = ?", (object.getRemainingRounds(), object.objectID))
        self.conn.commit()

    # Get a list of all cities
    def getAllCities(self):
        self.c.execute("select * from cities order by country")
        result = self.c.fetchall()
        return result

    # Unlock a city
    def unlockCity(self, cityid):
        self.c.execute("update cities set cityPrice = 0 where cityid = ?", [cityid])
        self.conn.commit()

    # Get current options
    def getOptions(self, deckname):
        self.c.execute("select option, optionDesc, value from options where deckname is ?", [deckname])
        result = self.c.fetchall()
        return result

    # Write a certain option to the database
    def setOption(self, deckname, option):
        self.c.execute("insert or replace into options(optionID, deckname, option, optionDesc, value) values((SELECT optionID FROM options WHERE deckname is ? AND option is ?), ?, ?, ?, ?)", (deckname, option.name, deckname, option.name, option.desc, option.getValue()))
        self.conn.commit()

    # Get all ranks for the specified type
    # type = 1: gold ranks
    # type = 2: construction ranks
    def getRanks(self, type):
        self.c.execute("select * from ranks where type = ? order by rankLimit ASC", [type])
        result = self.c.fetchall()

        return result

    # Get the latest stats entry
    def getStats(self, type):
        if type == 'latest':
            self.c.execute("select * from stats order by statsDay DESC LIMIT 1")
        elif type == 'record':
            self.c.execute("select * from stats order by cardsAnswered DESC LIMIT 1")
        result = self.c.fetchone()

        return result

    def saveStats(self, stats):
        self.c.execute("insert or replace into stats(statsID, statsDay, cardsAnswered) values((SELECT statsID FROM stats WHERE statsDay is ?), ?, ?)", (stats['statsDay'], stats['statsDay'], stats['cardsAnswered']))
        self.conn.commit()

    def __createDatabase(self):
        filename = getSqlPath('initialCreate.sql')

        if os.path.isfile(filename):
            f = codecs.open(filename, encoding='utf-8')
            sqlFile = f.read()
            self.c.executescript(sqlFile)
            self.conn.commit()

    # Install update if available
    def __updateDB(self):
        filename = getSqlPath('dsJapan.sql')

        if os.path.isfile(filename):
            f = codecs.open(filename, encoding='utf-8')
            sqlFile = f.read()

            if self.__hasFileChanged(sqlFile):
                self.c.executescript(sqlFile)
                self.conn.commit()

    # Checks if the update file has changed since last execution
    def __hasFileChanged(self, file):
        sqlHash = str(hash(file))
        # Read old hash from the database
        oldHash = self.readData('sqlHash')

        # Update the hash and return true if file has changed
        if oldHash is None or oldHash != sqlHash:
            self.writeData('sqlHash', sqlHash)
            return True
        else:
            return False

    def __del__(self):
        self.conn.commit()
        self.conn.close()
