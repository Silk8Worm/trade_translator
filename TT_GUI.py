"""
Download kivy: https://kivy.org/#download

GUI designed for the trade translator based on design:
https://www.figma.com/file/OKTVtYq4lWW2GOEMfP6k1t/Trade-Translator?node-id=17%3A0

Potential solution that helped me (Kevin):
https://github.com/kivy/kivy/issues/4991
"""

#TODO Graphing: https://github.com/kivy-garden/garden.graph

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout  # one of many layout structures
from kivy.uix.textinput import TextInput  # allow for ...text input.
from kivy.uix.button import Button

kivy.require("1.10.1")

# An actual app is likely to consist of many different
# "pages" or "screens." Inherit from GridLayout
class ConnectPage(GridLayout):
    # runs on initialization
    def __init__(self, **kwargs):
        # we want to run __init__ of both ConnectPage AAAAND GridLayout
        super().__init__(**kwargs)

        self.cols = 2  # used for our grid

        # widgets added in order, so mind the order.
        self.add_widget(Label(text='Email Address:'))  # widget #1, top left
        self.email = TextInput(multiline=False)  # defining self.ip...
        self.add_widget(self.email) # widget #2, top right

        self.add_widget(Label(text='Password:'))
        self.password = TextInput(multiline=False)
        self.add_widget(self.password)

        self.sign_in = Button(text="Sign In", size = (100, 200), pos = (50, 50))
        self.sign_in.bind(on_press=self.sign_in_button)
        self.add_widget(self.sign_in)

    def sign_in_button(self, instance):
        email = self.email.text
        password = self.password.text

        print(f"{email}, {password}")


class EpicApp(App):
    def build(self):
        return ConnectPage()


if __name__ == "__main__":
    EpicApp().run()
