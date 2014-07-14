import os.path
from aqt import mw
import sys

GOLD_ICON = 'gold.png'
ROUND_ICON = 'round.png'
STAR_ICON = 'star.png'
CONSTR_ICON = 'construction.png'
RANK_UP_ICON = 'rankup.png'
THUMBS_UP_ICON = 'thumbsup.png'

base = os.path.dirname(os.path.realpath(__file__))


def getAWFolder():
    try:
        folder = unicode(os.path.join(base, ''), sys.getfilesystemencoding())
    except:
        try:
            folder = unicode(os.path.join(base, ''), 'utf8')
        except:
            folder = os.path.join(base, '')
    return folder


def getSqlPath(sqlFile):
    return os.path.join(getAWFolder(), 'sql', '%s') % (sqlFile)


# Return the image folder
def getImagePath(cityname, image):
    return os.path.join(getAWFolder(), 'img', '%s', image) % (cityname)


def getMajorEventSound():
    return os.path.join(getAWFolder(), 'media', 'conq.mp3')


def getIcon(iconName):
    return os.path.join(getAWFolder(), 'media', iconName)


def getPluginName():
    return 'AnkiEmperor'


def getLogo():
    return '<img src="file:///%s" width="220">' % os.path.join(getAWFolder(), 'media', 'logo.png')


def getLinkColor():
    return 'style="color: #008B8B"'


def debug(debugText):
    from aqt.qt import QMessageBox
    QMessageBox.information(mw, getPluginName(), str(debugText))
