"""
Download kivy: https://kivy.org/#download

GUI designed for the trade translator based on design:
https://www.figma.com/file/OKTVtYq4lWW2GOEMfP6k1t/Trade-Translator?node-id=17%3A0

Potential solution to downloading Kivy that helped me (Kevin):
https://github.com/kivy/kivy/issues/4991
"""

#TODO Graphing: https://github.com/kivy-garden/garden.graph

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.widget import Widget
from kivy_garden.graph import Graph, MeshLinePlot
import os


class TradeTranslator(Screen):
    def do_signin(self, signinText, passwordText):
        app = App.get_running_app()

        app.username = signinText
        app.password = passwordText

        self.manager.transition = NoTransition()
        self.manager.current = 'trade'

    def do_signup(self, signinText, passwordText):
        app = App.get_running_app()

        app.username = signinText
        app.password = passwordText

        self.manager.transition = NoTransition()
        self.manager.current = 'signup'

    def resetForm(self):
        self.ids['signin'].text = ""
        self.ids['password'].text = ""


class SignUp(Screen):
    def create_account(self, email, password):
        self.manager.transition = NoTransition()
        self.manager.current = 'trade'

    def return_to_signin(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'signin'
        self.manager.get_screen('signin').resetForm()


class Trade(Screen):
    def disconnect(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'signin'
        self.manager.get_screen('signin').resetForm()

    def backtest(self, signal, trade, cover_signal, universe, take_profit, stop_loss, cover_trade):
        print("backtest")
        print(f'{signal},{trade},{cover_signal},{universe},{take_profit},{stop_loss},{cover_trade}')

        self.manager.current = 'backtest'

    def backtest_case(self, signal, trade, cover_signal, universe, take_profit, stop_loss, cover_trade):
        print("backtest case")
        print(f'{signal},{trade},{cover_signal},{universe},{take_profit},{stop_loss},{cover_trade}')

        self.manager.current = 'backtest'

    def account(self):
        print("Account page not set up.")


class BackTest(Screen):

    final_equity = StringProperty()
    cumulative_return = StringProperty()
    sharpe_ratio = StringProperty()
    sortino_ratio = StringProperty()

    def account(self):
        print("Account page not set up.")

        self.final_equity = '$5000'
        self.cumulative_return = '-50%'
        self.sharpe_ratio = '1.2'
        self.sortino_ratio = '2.3'

    def display_values(self):
        pass


class TradeTranslatorApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(TradeTranslator(name='signin'))
        manager.add_widget(Trade(name='trade'))
        manager.add_widget(SignUp(name='signup'))
        manager.add_widget(BackTest(name='backtest'))

        return manager


if __name__ == '__main__':
    TradeTranslatorApp().run()
