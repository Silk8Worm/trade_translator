"""
Download kivy: https://kivy.org/#download

GUI designed for the trade translator based on design:
https://www.figma.com/file/OKTVtYq4lWW2GOEMfP6k1t/Trade-Translator?node-id=17%3A0

Potential solution that helped me (Kevin):
https://github.com/kivy/kivy/issues/4991
"""

#TODO Graphing: https://github.com/kivy-garden/garden.graph

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import os

class Login(Screen):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        self.manager.transition = NoTransition()
        self.manager.current = 'connected'

        app.config.read(app.get_application_config())
        app.config.write()

    def do_signup(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        self.manager.transition = NoTransition()
        self.manager.current = 'signup'

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

class Connected(Screen):
    def disconnect(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

class SignUp(Screen):
    def create_account(self, email, password):
        print(email)
        print(password)
        self.manager.transition = NoTransition()
        self.manager.current = 'connected'

    def return_to_login(self):
        self.manager.transition = NoTransition()
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        manager.add_widget(SignUp(name='signup'))

        return manager

    def get_application_config(self):
        if(not self.username):
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

if __name__ == '__main__':
    LoginApp().run()
