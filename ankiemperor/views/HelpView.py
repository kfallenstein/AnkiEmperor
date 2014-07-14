from ankiemperor.util import *


class HelpView(object):

    def __init__(self, ae):
        pass

    def help(self):

        html = '''<h1>AnkiEmperor Help</h1>

            <style type='text/css'>
                table.alternate tr:nth-child(odd)   { background-color:#f3f3f3; }
                table.alternate tr:nth-child(even)    { background-color:#e7e7e7; }
            </style>

            <p>AnkiEmperor is a add-on to add another level of fun to reviewing cards in Anki by providing a game-like scenario.</p>
            <p>As you earn more gold and build more constructions, your rank will improve.
How long will it take you to become Emperor?</p>

            <h3>Gold <img src="file:///%s"></h3>
            <p>Earn gold by answering cards. Gold can be used to unlock new cities and build constructions (such as parks, skyscapers, famous sightseeing spots) within these cities.</p>

            <p>Your answer to a card, determines how much gold you get:</p>

            <table width='100%%' class='alternate' cellspacing='0' cellpadding='3'>
                <tr>
                <th align='left'>New card queue</th>
                <th align='right'>Gold</th>
                </tr>
                <tr>
                    <td>Easy</td>
                    <td align='right'>18</td>
                </tr>
                <tr>
                    <td>Good</td>
                    <td align='right'>16</td>
                </tr>
                <tr>
                    <td>Again</td>
                    <td align='right'>12</td>
                </tr>
            </table>

            <table width='100%%' class='alternate' cellspacing='0' cellpadding='3'>
                <tr>
                <th align='left'>Learning queue</th>
                </tr>
                <tr>
                    <td>Good</td>
                    <td align='right'>6</td>
                </tr>
                <tr>
                    <td>Again</td>
                    <td align='right'>2</td>
                </tr>
            </table>

            <table width='100%%' class='alternate' cellspacing='0' cellpadding='3'>
                <tr>
                <th align='left'>Review Queue</th>
                </tr>
                <tr>
                    <td>Easy</td>
                    <td align='right'>10</td>
                </tr>
                <tr>
                    <td>Good</td>
                    <td align='right'>8</td>
                </tr>
                <tr>
                    <td>Hard</td>
                    <td align='right'>6</td>
                </tr>
                <tr>
                    <td>Again</td>
                    <td align='right'>2</td>
                </tr>
            </table>

            <p>Your gold is reduced after answering a certain amount of cards (resets daily).</p>

            <table width='100%%' class='alternate' cellspacing='0' cellpadding='3'>
                <tr>
                <th align='left'>Cards</th>
                <th align='right'>Reduction</th>
                </tr>
                <tr>
                    <td>50 - 99</td>
                    <td align='right'>25%%</td>
                </tr>
                <tr>
                    <td>100 - 199</td>
                    <td align='right'>50%%</td>
                </tr>
                <tr>
                    <td>200+</td>
                    <td align='right'>75%%</td>
                </tr>
            </table>

            <h3>Rounds <img src="file:///%s"></h3>
            <p>Rounds determine how long it will take to complete a construction.</p>
            <p>Every card you get correct will advance you a round.<p>
            <p>After 100 cards, every two cards you get correct will advance you a round.</p>

            <br><a href="MainView||main">&lt;&lt; Back to main view</a>
        ''' % (getIcon(GOLD_ICON), getIcon(ROUND_ICON))
        return html
