from aqt import mw
from aqt.qt import *
from ankiemperor.util import *
from ankiemperor.Options import *


class SettingsView(object):

    def __init__(self, ae):

        # Get options
        self.options = ae.getOptions()

        self.deckSelected = ae.deckSelected

        self.ae = ae

    def settings(self):
        html = "<h1>%s Settings</h1>" % getPluginName()
        html += '<h2>Global options</h2>'
        html += '<table>'
        for key, option in self.options.getGlobalOptions().iteritems():
            if isinstance(option, BooleanOption):
                html += '<tr><td width="140">%s [<a href="SettingsView||showDescription||%s||%s">?</a>]:</td><td><a href="SettingsView||changeGlobalOption||%s">%s</a></td></tr>' % (option.desc, option.desc, option.longDesc, key, option.getValue())
            else:
                html += '<tr><td width="140">%s [<a href="SettingsView||showDescription||%s||%s">?</a>]:</td><td>%s</td></tr>' % (option.desc, option.desc, option.longDesc, option.getValue())
        html += '</table>'

        if (self.deckSelected):
            html += '<h2>Current deck options</h2>'
            html += '<table>'
            for key, option in self.options.getDeckOptions().iteritems():
                html += '<tr><td width="140">%s [<a href="SettingsView||showDescription||%s||%s"">?</a>]:</td><td><a href="SettingsView||changeDeckOption||%s">%s</a></td></tr>' % (option.desc, option.desc, option.longDesc, key, option.getValue())
            html += '</table><br>'

        html += '<br /><a href="MainView||main">&lt;&lt; Back to main view</a>'

        return html

    # Change a deck option
    def changeDeckOption(self, optionKey):
        option = self.options.getDeckOptions()[optionKey]
        self.options.changeDeckOption(optionKey, not option.getValue())
        self.ae.setView("SettingsView||settings")
        return self.settings()

    # Change a global option
    def changeGlobalOption(self, optionKey):
        option = self.options.getGlobalOptions()[optionKey]
        self.options.changeGlobalOption(optionKey, not option.getValue())
        self.ae.setView("SettingsView||settings")
        return self.settings()

    def showDescription(self, optionDesc, optionLongDesc):
        QMessageBox.information(mw, 'Option: %s' % optionDesc, '%s' % optionLongDesc)
        self.ae.setView("SettingsView||settings")
