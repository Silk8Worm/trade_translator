"""
Download kivy: https://kivy.org/#download

GUI designed for the trade translator based on design:
https://www.figma.com/file/OKTVtYq4lWW2GOEMfP6k1t/Trade-Translator?node-id=17%3A0

Potential solution to downloading Kivy that helped me (Kevin):
https://github.com/kivy/kivy/issues/4991
"""

#TODO Graphing: https://github.com/kivy-garden/garden.graph

import kivy
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
# Use this if you need to import TextInput
# from kivy.core.window import Window
from kivy.config import Config # Better implementation of window size
from kivy.clock import Clock
from functools import partial
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

    word_list = "this is a test for suggestion text".split(' ')

    def disconnect(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'signin'
        self.manager.get_screen('signin').resetForm()

    def backtest(self, signal, trade, cover_signal, universe, take_profit, stop_loss, cover_trade):
        print("backtest")
        print(f'{signal},{trade},{cover_signal},{universe},{take_profit},{stop_loss},{cover_trade}')

        self.manager.current = 'backtest'
        self.manager.get_screen('backtest').chart(5000, 10000, 1.4, 2.3, [1,2,3], [1,4,9])

    def backtest_case(self, signal, trade, cover_signal, universe, take_profit, stop_loss, cover_trade):
        print("backtest case")
        print(f'{signal},{trade},{cover_signal},{universe},{take_profit},{stop_loss},{cover_trade}')

        self.manager.current = 'backtest'
        self.manager.get_screen('backtest').chart(5000, 10000, 1.4, 2.3, [1,2,3], [5,6,7])

    def account(self):
        print("Account page not set up.")

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
        instance.cursor = (len(instance.text), 0)

class BackTest(Screen):

    final_equity = StringProperty()
    cumulative_return = StringProperty()
    sharpe_ratio = StringProperty()
    sortino_ratio = StringProperty()
    image = StringProperty()

    def account(self):
        print("Account page not set up.")

    def chart(self, final: float, cumulative: float, sharpe: float, sortino: float, x_vals: [], y_vals: []):

        self.final_equity = f'${final:.2f}'
        self.cumulative_return = f'${cumulative:.2f}'
        self.sharpe_ratio = f'{sharpe:.3f}'
        self.sortino_ratio = f'{sortino:.3f}'

        fig, ax = plt.subplots(figsize=(14,6.2))
        plt.plot(x_vals, y_vals)
        plt.savefig('chart.png', bbox_inches='tight')
        self.image = 'chart.png'


class TradeTranslatorApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):

        self.title = "Trade Translator"

        # Better implementation of window size
        Config.set('graphics','resizable', True)
        Config.set('graphics', 'width', 1100)
        Config.set('graphics', 'height', 720)
        Config.set('graphics', 'minimum_width', '1100')
        Config.set('graphics', 'minimum_height', '720')
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

        manager = ScreenManager()

        manager.add_widget(TradeTranslator(name='signin'))
        manager.add_widget(Trade(name='trade'))
        manager.add_widget(SignUp(name='signup'))
        manager.add_widget(BackTest(name='backtest'))

        # Use this if you need to import TextInput
        # Window.size = (1100, 720)
        # Window.minimum_width, Window.minimum_height = Window.size
        # Window.left = Window.left-150
        # Window.top = Window.top-60


        return manager


if __name__ == '__main__':
    TradeTranslatorApp().run()
