"""
Download kivy: https://kivy.org/#download

GUI designed for the trade translator based on design:
https://www.figma.com/file/OKTVtYq4lWW2GOEMfP6k1t/Trade-Translator?node-id=17%3A0

Potential solution to downloading Kivy that helped me (Kevin):
https://github.com/kivy/kivy/issues/4991
"""

from kivy.app import App
from kivy.lang import Builder
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
from datetime import timedelta
import requests
import time
import Zippy

class TradeTranslator(Screen):

    login_error = BooleanProperty(False)

    def do_signin(self, signinText, passwordText):
        app = App.get_running_app()

        app.username = signinText
        app.password = passwordText

        r = requests.post('https://tranquil-beyond-74281.herokuapp.com/info/validate/', data={'username':app.username, 'password':app.password})
        if r.text == 'true':
            self.manager.transition = NoTransition()
            self.manager.current = 'trade'
        else:
            self.login_error = True

    def resetForm(self):
        self.ids['signin'].text = ""
        self.ids['password'].text = ""

class Trade(Screen):

    suggestion_words = "atr rsi obv macd".split(' ')
    word_list = suggestion_words.copy()
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
            self.word_list))
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
        popup = ErrorPopup()
        popup.open()
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


class ErrorPopup(Popup):
    pass


class BackTestPopup(Popup):

    def backtest(self, first_date, second_date):

        try:
            date1test = datetime.strptime(first_date, '%d/%m/%Y')
            date2test = datetime.strptime(second_date, '%d/%m/%Y')
            if date2test <= date1test:
                app = App.get_running_app()
                Trade.error_text(app.manager.get_screen('trade'), 'Backtest Dates', ['Start date must be before end date.'])
                return
            date1test += timedelta(days=7)
            if date2test < date1test:
                app = App.get_running_app()
                Trade.error_text(app.manager.get_screen('trade'), 'Backtest Dates', ['Date range not large enough (min 1 week).'])
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
            app.manager.get_screen('backtest').submit_enabled = False


class CasePopup(Popup):

    # Set True to False to disable cases
    case_enabled = BooleanProperty(True)
    case_name = StringProperty()
    casestart = ""
    caseend = ""

    def __init__(self, **kwargs):
        super(Popup, self).__init__(**kwargs)
        r = requests.get('https://tranquil-beyond-74281.herokuapp.com/info/cases/get/')
        if len(r.json()['cases']) == 0:
            self.case_enabled = False
        else:
            self.case_name = r.json()['cases'][0]['name']
            self.casestart = r.json()['cases'][0]['startDate']
            self.caseend = r.json()['cases'][0]['endDate']

    def case(self):
        a, b, c, d = Zippy.zippy(self.signal,self.buy,self.trade,
                                 self.cover_signal,self.universe,
                                 self.take_profit,self.stop_loss,
                                 self.cover_buy,self.cover_trade,
                                 self.casestart, self.caseend)

        if a in ['Invalid Input', 'Invalid Ticker List', 'No Tickers Entered']:
            app = App.get_running_app()
            Trade.error_text(app.manager.get_screen('trade'), b, c)
        else:
            app = App.get_running_app()
            app.manager.get_screen('backtest').chart(a, b, c, d)
            app.manager.get_screen('backtest').submit_enabled = True
            app.manager.get_screen('backtest').casename = self.case_name
            app.manager.current = 'backtest'


class BackTest(Screen):

    final_equity = StringProperty()
    cumulative_return = StringProperty()
    sharpe_ratio = StringProperty()
    sortino_ratio = StringProperty()
    image = StringProperty()
    submit_enabled = BooleanProperty(True)
    submit_text = StringProperty()

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.infinite_sortino = False
        self.submit_text = 'SUBMIT'

    def back(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'trade'
        self.image = 'logo.png'

    def chart(self, final: float, cumulative: float, sharpe: float, sortino: float):

        self.final_equity = f'${final:.2f}'
        self.cumulative_return = f'${cumulative:.2f}'
        self.sharpe_ratio = f'{sharpe:.3f}'
        if sortino == 100000:
            self.sortino_ratio = 'Infinity'
            self.infinite_sortino = True
        else:
            self.sortino_ratio = f'{sortino:.3f}'
        Cache._categories['kv.image']['limit'] = 0
        Cache._categories['kv.image']['timeout'] = 1
        Cache._categories['kv.texture']['limit'] = 0
        Cache._categories['kv.texture']['timeout'] = 1
        self.image = 'chart.png'

    def submit(self):
        app = App.get_running_app()
        if self.sortino_ratio == 'Infinity':
            sortino_submit = 0
        else:
            sortino_submit = float(self.sortino_ratio)
        r = requests.post('https://tranquil-beyond-74281.herokuapp.com/info/cases/submit/',
                          data={"username": app.username, "case": self.casename,
                                "equity": float(self.final_equity.strip('$')),
                                "return": float(self.cumulative_return.strip('$')),
                                "sortino": sortino_submit,
                                "sharpe": float(self.sharpe_ratio),
                                'infinite_sortino': self.infinite_sortino})
        if r.text == 'false':
            self.submit_text = 'ERROR'


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

        self.manager.add_widget(Trade(name='trade'))
        self.manager.add_widget(BackTest(name='backtest'))
        self.manager.add_widget(TradeTranslator(name='signin'))

        # Use this if you need to import TextInput
        # Window.size = (1100, 720)
        # Window.minimum_width, Window.minimum_height = Window.size
        # Window.left = Window.left-150
        # Window.top = Window.top-60

        return self.manager
