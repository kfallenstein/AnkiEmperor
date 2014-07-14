from ankiemperor.AnkiEmperor import AnkiEmperor
from anki.hooks import *

ae = AnkiEmperor()
addHook("profileLoaded", ae.onProfileLoaded)
