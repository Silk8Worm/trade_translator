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
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy_garden.graph import Graph, MeshLinePlot
import os
from matplotlib import pyplot as plt


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
        self.manager.get_screen('backtest').chart(5000, .5, 1.4, 2.3, [1,2,3], [5,6,7])

    def backtest_case(self, signal, trade, cover_signal, universe, take_profit, stop_loss, cover_trade):
        print("backtest case")
        print(f'{signal},{trade},{cover_signal},{universe},{take_profit},{stop_loss},{cover_trade}')

        self.manager.current = 'backtest'
        self.manager.get_screen('backtest').chart(5000, .5, 1.4, 2.3, [1,2,3], [5,6,7])

    def account(self):
        print("Account page not set up.")


class BackTest(Screen):

    final_equity = StringProperty()
    cumulative_return = StringProperty()
    sharpe_ratio = StringProperty()
    sortino_ratio = StringProperty()
    image = StringProperty()

    def account(self):
        print("Account page not set up.")

    def display_values(self):
        pass

    def chart(self, final: float, cumulative: float, sharpe: float, sortino: float, x_vals: [], y_vals: []):

        self.final_equity = f'${final}'
        self.cumulative_return = f'{cumulative*100}%'
        self.sharpe_ratio = f'{sharpe}'
        self.sortino_ratio = f'{sortino}'

        plt.plot(x_vals, y_vals)

        plt.savefig('chart.png', bbox_inches='tight')
        self.image = 'chart.png'


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
    Config.set('graphics','resizable', False)
    Config.set('graphics', 'width', 1100)
    Config.set('graphics', 'height', 720)
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    TradeTranslatorApp().run()
