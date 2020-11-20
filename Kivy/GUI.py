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

    lower_words = 'atr above and bbands below close crosses debt debt/ebitda day days ema ebitda equal greater growth high if is low leverage less macd margin month months net obv open operating or rsi revenue ratio sma than to volume yesterday years year'
    upper_words = lower_words.upper()
    suggestion_words = (lower_words+' '+upper_words).split()
    word_list = suggestion_words.copy()
    # Number Text
    trade = StringProperty()
    cover_trade = StringProperty()
    trade_hint = StringProperty()
    cover_trade_hint = StringProperty()
    # Signal Text
    trade_text = StringProperty()
    cover_text = StringProperty()
    universe_text = StringProperty()

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.trade = "Buy #"
        self.cover_trade = "Sell #"
        self.trade_hint = "Enter # of shares"
        self.cover_trade_hint = "Enter # of shares"

    def change_trade(self):
        if self.trade == "Buy #":
            self.trade = "Buy %"
            self.trade_hint = "Enter % of portfolio"
        elif self.trade == "Buy %":
            self.trade = "Sell #"
            self.trade_hint = "Enter # of shares"
        elif self.trade == "Sell #":
            self.trade = "Sell %"
            self.trade_hint = "Enter % of portfolio"
        elif self.trade == "Sell %":
            self.trade = "Buy #"
            self.trade_hint = "Enter # of shares"
        else:
            print("Error with button.")

    def change_cover_trade(self):
        if self.cover_trade == "Buy #":
            self.cover_trade = "Buy %"
            self.cover_trade_hint = "Enter % of portfolio"
        elif self.cover_trade == "Buy %":
            self.cover_trade = "Sell #"
            self.cover_trade_hint = "Enter # of shares"
        elif self.cover_trade == "Sell #":
            self.cover_trade = "Sell %"
            self.cover_trade_hint = "Enter % of portfolio"
        elif self.cover_trade == "Sell %":
            self.cover_trade = "Buy #"
            self.cover_trade_hint = "Enter # of shares"
        else:
            print("Error with button.")

    def backtest(self, signal, trade, cover_signal, universe, take_profit, stop_loss, cover_trade):
        popup = BackTestPopup()
        popup.open()
        popup.signal = signal
        if self.trade in ['Buy %', 'Sell %']:
            popup.trade = trade + '%'
        else:
            popup.trade = trade
        popup.cover_signal = cover_signal
        popup.universe = universe
        popup.take_profit = take_profit
        popup.stop_loss = stop_loss
        if self.cover_trade in ['Buy %', 'Sell %']:
            popup.cover_trade = cover_trade + '%'
        else:
            popup.cover_trade = cover_trade
        popup.buy = self.trade
        popup.cover_buy = self.cover_trade

    def backtest_case(self, signal, trade, cover_signal, universe, take_profit, stop_loss, cover_trade):
        popup = CasePopup()
        popup.open()
        popup.signal = signal
        if self.trade in ['Buy %', 'Sell %']:
            popup.trade = trade + '%'
        else:
            popup.trade = trade
        popup.cover_signal = cover_signal
        popup.universe = universe
        popup.take_profit = take_profit
        popup.stop_loss = stop_loss
        if self.cover_trade in ['Buy %', 'Sell %']:
            popup.cover_trade = cover_trade + '%'
        else:
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
        word_list = self.word_list
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

    def error_text(self, text: str, module: str, errors: []):
        popup = ErrorPopup(module, text, errors)
        popup.error_module = module
        popup.error_text = text
        popup.errors_lst = errors
        popup.open()


class ErrorPopup(Popup):
    error_module = StringProperty()
    error_text = StringProperty()
    errors = StringProperty()

    def __init__(self, module, text, errors, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.error_module = module
        self.error_text = text
        self.errors_lst = errors
        if self.error_module == 'Signal' or self.error_module == 'Cover Signal':
            if self.errors_lst[0][1] == -1:
                self.errors = 'Input too short. Missing words.'
            else:
                self.errors = self.errors_lst[0][2] + '(s): '
                for i in range(len(self.errors_lst)):
                    self.errors += str(self.errors_lst[i][0])
                    if i < len(self.errors_lst) - 1:
                        self.errors += ', '
        elif self.error_module == 'Universe':
            if self.errors_lst == []:
                self.errors = "No universe entered."
            else:
                self.errors = "Invalid ticker(s): "
                for i in range(len(self.errors_lst)):
                    self.errors += self.errors_lst[i]
                    if i < len(self.errors_lst) - 1:
                        self.errors += ', '
        elif self.error_module == 'Backtest Dates':
            if text == ' - ':
                self.errors = 'No date provided.'
            else:
                self.errors = self.errors_lst[0]
        elif self.error_module in ['Take Profit', 'Stop Loss', 'Trade', 'Cover Trade']:
            self.errors = "You cannot enter a negative number."
        else:
            print("Module does not exist")


class BackTestPopup(Popup):

    def backtest(self, first_date, second_date):

        try:
            date1test = datetime.strptime(first_date, '%d/%m/%Y')
            date2test = datetime.strptime(second_date, '%d/%m/%Y')
            if date2test <= date1test:
                app = App.get_running_app()
                Trade.error_text(app.manager.get_screen('trade'), first_date+' - '+second_date, 'Backtest Dates', ['Start date must be before end date and at least 1 week before.'])
                return
            date1test += timedelta(days=7)
            if date2test < date1test:
                app = App.get_running_app()
                Trade.error_text(app.manager.get_screen('trade'), first_date+' - '+second_date, 'Backtest Dates', ['Date range not large enough (min 1 week).'])
                return
            earliest_date = datetime(2018, 11, 1)
            if earliest_date > date1test:
                app = App.get_running_app()
                Trade.error_text(app.manager.get_screen('trade'), first_date+' - '+second_date, 'Backtest Dates', ['Currently, we only support backtesting starting from Nov. 1st, 2018.'])
                return
        except:
            app = App.get_running_app()
            Trade.error_text(app.manager.get_screen('trade'), first_date+' - '+second_date, 'Backtest Dates', ['Invalid date format.'])
            return

        a, b, c, d, e = Zippy.zippy(self.signal,self.buy,self.trade,
                                 self.cover_signal,self.universe,
                                 self.take_profit,self.stop_loss,
                                 self.cover_buy,self.cover_trade,
                                 first_date, second_date)

        if a in ['Invalid Input', 'Invalid Ticker List', 'No Tickers Entered', 'Negative Values Not Accepted']:
            app = App.get_running_app()
            Trade.error_text(app.manager.get_screen('trade'), d, b, c)
        else:
            app = App.get_running_app()
            app.manager.transition = NoTransition()
            app.manager.current = 'backtest'
            app.manager.get_screen('backtest').chart(a, b, c, d)
            app.manager.get_screen('backtest').submit_enabled = False
            app.manager.get_screen('backtest').submit_text = 'SUBMIT'


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
        a, b, c, d, e = Zippy.zippy(self.signal,self.buy,self.trade,
                                 self.cover_signal,self.universe,
                                 self.take_profit,self.stop_loss,
                                 self.cover_buy,self.cover_trade,
                                 self.casestart, self.caseend)

        if a in ['Invalid Input', 'Invalid Ticker List', 'No Tickers Entered', 'Negative Values Not Accepted']:
            app = App.get_running_app()
            Trade.error_text(app.manager.get_screen('trade'), d, b, c)
        else:
            app = App.get_running_app()
            app.manager.transition = NoTransition()
            app.manager.get_screen('backtest').chart(a, b, c, d)
            app.manager.get_screen('backtest').submit_enabled = True
            app.manager.get_screen('backtest').casename = self.case_name
            app.manager.get_screen('backtest').universe = self.universe
            app.manager.get_screen('backtest').signal = self.signal
            app.manager.get_screen('backtest').cover_signal = self.cover_signal
            app.manager.get_screen('backtest').enter_instruction = self.buy
            app.manager.get_screen('backtest').exit_instruction = self.cover_buy
            app.manager.get_screen('backtest').take_profit = self.take_profit
            app.manager.get_screen('backtest').stop_loss = self.stop_loss
            app.manager.get_screen('backtest').signal_amount = self.trade
            app.manager.get_screen('backtest').cover_signal_amount = self.cover_trade
            app.manager.get_screen('backtest').transaction_history = e
            app.manager.get_screen('backtest').submit_text = 'SUBMIT'
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
        self.image = 'Kivy/chart.png'

    def submit(self):
        app = App.get_running_app()
        self.signal_amount = self.signal_amount.strip('%')
        self.cover_signal_amount = self.cover_signal_amount.strip('%')
        if self.take_profit == '':
            self.take_profit = '0'
        if self.stop_loss == '':
            self.stop_loss = '0'
        if self.signal_amount == '':
            self.signal_amount = '0'
        if self.cover_signal_amount == '':
            self.cover_signal_amount = '0'
        if self.sortino_ratio == 'Infinity':
            sortino_submit = 0
        else:
            sortino_submit = float(self.sortino_ratio)
        r = requests.post('https://tranquil-beyond-74281.herokuapp.com/info/cases/ext-submit/',
                          data={"username": app.username, "case": self.casename,
                                "equity": float(self.final_equity.strip('$')),
                                "return": float(self.cumulative_return.strip('$')),
                                "sortino": sortino_submit,
                                "sharpe": float(self.sharpe_ratio),
                                "universe": self.universe,
                                "signal": self.signal,
                                "cover_signal": self.cover_signal,
                                "enter_instruction": self.enter_instruction,
                                "exit_instruction": self.exit_instruction,
                                "take_profit": float(self.take_profit),
                                "stop_loss": float(self.stop_loss),
                                "signal_amount": int(self.signal_amount),
                                "cover_signal_amount": int(self.cover_signal_amount),
                                "transaction_history": ', '.join(self.transaction_history),
                                "infinite_sortino": self.infinite_sortino})
        print(r.text)
        if r.text.lower() == 'false':
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

        self.manager.add_widget(TradeTranslator(name='signin'))
        self.manager.add_widget(Trade(name='trade'))
        self.manager.add_widget(BackTest(name='backtest'))

        # Use this if you need to import TextInput
        # Window.size = (1100, 720)
        # Window.minimum_width, Window.minimum_height = Window.size
        # Window.left = Window.left-150
        # Window.top = Window.top-60

        return self.manager
