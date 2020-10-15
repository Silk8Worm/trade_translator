"""
Download kivy: https://kivy.org/#download

GUI designed for the trade translator based on design:
https://www.figma.com/file/OKTVtYq4lWW2GOEMfP6k1t/Trade-Translator?node-id=17%3A0

Potential solution to downloading Kivy that helped me (Kevin):
https://github.com/kivy/kivy/issues/4991
"""

from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.popup import Popup
# Use this if you need to import TextInput
# from kivy.core.window import Window
from kivy.config import Config # Better implementation of window size
from kivy.clock import Clock
from functools import partial
from kivy.cache import Cache
from datetime import datetime
import Zippy


class TradeTranslator(Screen):
    def do_signin(self, signinText, passwordText):
        app = App.get_running_app()

        app.username = signinText
        app.password = passwordText

        self.manager.transition = NoTransition()
        self.manager.current = 'trade'

    def resetForm(self):
        self.ids['signin'].text = ""
        self.ids['password'].text = ""

class Trade(Screen):

    word_list = "atr rsi obv macd".split(' ')
    trade = StringProperty()
    cover_trade = StringProperty()
    trade_text = StringProperty()
    cover_text = StringProperty()
    universe_text = StringProperty()

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.trade = "Buy"
        self.cover_trade = "Sell"

    def change_trade(self):
        if self.trade == "Buy":
            self.trade = "Sell"
        else:
            self.trade = "Buy"

    def change_cover_trade(self):
        if self.cover_trade == "Buy":
            self.cover_trade = "Sell"
        else:
            self.cover_trade = "Buy"

    def disconnect(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'signin'
        self.manager.get_screen('signin').resetForm()

    def backtest(self, signal, trade, cover_signal, universe, take_profit, stop_loss, cover_trade):
        popup = BackTestPopup()
        popup.open()
        popup.signal = signal
        popup.trade = trade
        popup.cover_signal = cover_signal
        popup.universe = universe
        popup.take_profit = take_profit
        popup.stop_loss = stop_loss
        popup.cover_trade = cover_trade
        popup.buy = self.trade
        popup.cover_buy = self.cover_trade

    def backtest_case(self, signal, trade, cover_signal, universe, take_profit, stop_loss, cover_trade):
        popup = CasePopup()
        popup.open()
        popup.signal = signal
        popup.trade = trade
        popup.cover_signal = cover_signal
        popup.universe = universe
        popup.take_profit = take_profit
        popup.stop_loss = stop_loss
        popup.cover_trade = cover_trade
        popup.buy = self.trade
        popup.cover_buy = self.cover_trade

    def on_text(self, instance, value):
        """ Include all current text from textinput into the word list to
        emulate the same kind of behavior as sublime text has.
        """
        if '	' in value and instance.suggestion_text:
            instance.text = value.replace('	', '')
            instance.insert_text(instance.suggestion_text + ' ')
            Clock.schedule_once(partial(self.set_cursor, instance), 0)
            return
        elif '	' in value:
            instance.text = value.replace('	', '')
            return
        instance.suggestion_text = ' '
        word_list = list(set(
            self.word_list + value[:value.find(' ')].split(' ')))
        val = value[value.rfind(' ') + 1:]
        if not val:
            return
        try:
            word = [word for word in word_list
                    if word.startswith(val)][0][len(val):]
            if not word:
                return
            instance.suggestion_text = word
        except IndexError:
            pass

    def set_cursor(self, instance, dt):
        instance.cursor = (len(instance.text), 50)

    def error_text(self, module: str, errors: []):
        if module == 'Signal':
            self.trade_text = "Fuck"
            print(errors)
        elif module == 'Cover':
            self.cover_text = "Fuck"
            print(errors)
        elif module == 'Universe':
            self.universe_text = "Fuck"
            print(errors)
        else:
            print("Module does not exist")


class BackTestPopup(Popup):

    def backtest(self, first_date, second_date):

        try:
            date1test = datetime.strptime(first_date, '%d/%m/%Y')
            date2test = datetime.strptime(second_date, '%d/%m/%Y')
            if date2test <= date1test:
                print("Start date must be before end date.")
                return
        except:
            print("Invalid Date Format")
            return

        a, b, c, d = Zippy.zippy(self.signal,self.buy,self.trade,
                                 self.cover_signal,self.universe,
                                 self.take_profit,self.stop_loss,
                                 self.cover_buy,self.cover_trade,
                                 first_date, second_date)

        if a in ['Invalid Input', 'Invalid Ticker List', 'No Tickers Entered']:
            app = App.get_running_app()
            Trade.error_text(app.manager.get_screen('trade'), b, c)
        else:
            app = App.get_running_app()
            app.manager.current = 'backtest'
            app.manager.get_screen('backtest').chart(a, b, c, d)


class CasePopup(Popup):

    # Set True to False to disable cases
    case1enabled = BooleanProperty(True)
    case2enabled = BooleanProperty(True)
    case3enabled = BooleanProperty(False)

    case1start = "01/01/2020"
    case1end = "10/03/2020"
    case2start = "01/01/2020"
    case2end = "12/01/2020"
    case3start = "01/01/2020"
    case3end = "14/01/2020"

    def case1(self):
        a, b, c, d = Zippy.zippy(self.signal,self.buy,self.trade,
                                 self.cover_signal,self.universe,
                                 self.take_profit,self.stop_loss,
                                 self.cover_buy,self.cover_trade,
                                 self.case1start, self.case1end)

        if a in ['Invalid Input', 'Invalid Ticker List', 'No Tickers Entered']:
            app = App.get_running_app()
            Trade.error_text(app.manager.get_screen('trade'), b, c)
        else:
            app = App.get_running_app()
            app.manager.current = 'backtest'
            app.manager.get_screen('backtest').chart(a, b, c, d)

    def case2(self):
        a, b, c, d = Zippy.zippy(self.signal,self.buy,self.trade,
                                 self.cover_signal,self.universe,
                                 self.take_profit,self.stop_loss,
                                 self.cover_buy,self.cover_trade,
                                 self.case2start, self.case2end)

        if a in ['Invalid Input', 'Invalid Ticker List', 'No Tickers Entered']:
            app = App.get_running_app()
            Trade.error_text(app.manager.get_screen('trade'), b, c)
        else:
            app = App.get_running_app()
            app.manager.current = 'backtest'
            app.manager.get_screen('backtest').chart(a, b, c, d)

    def case3(self):
        a, b, c, d = Zippy.zippy(self.signal,self.buy,self.trade,
                                 self.cover_signal,self.universe,
                                 self.take_profit,self.stop_loss,
                                 self.cover_buy,self.cover_trade,
                                 self.case3start, self.case3end)

        if a in ['Invalid Input', 'Invalid Ticker List', 'No Tickers Entered']:
            app = App.get_running_app()
            Trade.error_text(app.manager.get_screen('trade'), b, c)
        else:
            app = App.get_running_app()
            app.manager.current = 'backtest'
            app.manager.get_screen('backtest').chart(a, b, c, d)


class BackTest(Screen):

    final_equity = StringProperty()
    cumulative_return = StringProperty()
    sharpe_ratio = StringProperty()
    sortino_ratio = StringProperty()
    image = StringProperty()

    def back(self):
        self.manager.current = 'trade'
        self.image = 'logo.png'

    def chart(self, final: float, cumulative: float, sharpe: float, sortino: float):

        self.final_equity = f'${final:.2f}'
        self.cumulative_return = f'${cumulative:.2f}'
        self.sharpe_ratio = f'{sharpe:.3f}'
        self.sortino_ratio = f'{sortino:.3f}'
        Cache._categories['kv.image']['limit'] = 0
        Cache._categories['kv.image']['timeout'] = 1
        Cache._categories['kv.texture']['limit'] = 0
        Cache._categories['kv.texture']['timeout'] = 1
        self.image = 'chart.png'


class TradeTranslatorApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):

        self.title = "Rotman Commerce FinTech Association"

        # Better implementation of window size
        Config.set('graphics','resizable', True)
        Config.set('graphics', 'width', 1135)
        Config.set('graphics', 'height', 640)
        Config.set('graphics', 'minimum_width', '1135')
        Config.set('graphics', 'minimum_height', '640')
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

        self.manager = ScreenManager()

        self.manager.add_widget(TradeTranslator(name='signin'))
        self.manager.add_widget(Trade(name='trade'))
        self.manager.add_widget(BackTest(name='backtest'))

        # Use this if you need to import TextInput
        # Window.size = (1100, 720)
        # Window.minimum_width, Window.minimum_height = Window.size
        # Window.left = Window.left-150
        # Window.top = Window.top-60

        return self.manager


if __name__ == '__main__':
    TradeTranslatorApp().run()
