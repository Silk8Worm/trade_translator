# Adds back compatibility for python2
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from sys import stderr, exc_info

import platform

# Move into the correct working directory
import os
os.chdir(os.getcwd()+"/trade_translator-master")

WINDOWS = "Windows10"
if platform.system() + platform.release() != WINDOWS:
    print("You must run on Windows 10", file=stderr)
    exit(1)

if platform.system() + platform.release() != WINDOWS:
    print("You must run on Windows 10", file=stderr)
    exit(1)

PYTHON_VERSION = '3.8.6'
if platform.python_version() != PYTHON_VERSION:
    print(
        platform.python_version() + " does not work with the application. You must run using Python " + PYTHON_VERSION,
        file=stderr)
    exit(1)

# Check that the critical modules are have the correct versions
try:
    import kivy
    KIVY_VERSION = '2.0.0rc4'
    if kivy.__version__ != KIVY_VERSION:
        print("You are running the wrong version of Kivy. You need " + KIVY_VERSION, file=stderr)
        exit(1)

    import backtrader
    BACKTRADER_VERSION = '1.9.76.123'
    if backtrader.__version__ != BACKTRADER_VERSION:
        print("You are running the wrong version of Backtrader. You need " + BACKTRADER_VERSION, file=stderr)
        exit(1)

    import ply
    PLY_VERSION = '3.11'
    if ply.__version__ != PLY_VERSION:
        print("You are running the wrong version of PLY. You need " + PLY_VERSION, file=stderr)
        exit(1)
except ImportError:
    print("There was a problem import one of the critical modules", file=stderr)
    print(exc_info(), file=stderr)
    exit(1)

# If you have the correct version of all the modules and python, then startup the app
from Kivy.GUI import TradeTranslatorApp
TradeTranslatorApp().run()
