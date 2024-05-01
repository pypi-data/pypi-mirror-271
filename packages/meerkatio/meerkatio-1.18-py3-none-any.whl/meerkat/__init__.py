import os
import time
import importlib.resources as resources
from IPython.core.magic import Magics, magics_class, line_magic
from IPython import get_ipython

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer

from meerkat.api import send_meerkat_notification

module_runtime = int(time.time()*1000)

if not os.environ.get("MEERKAT_TOKEN"):
    try:
        with open(os.path.expanduser("~") + "/.meerkat") as file:
            os.environ["MEERKAT_TOKEN"] = file.read()
    except Exception as e:
        pass

def _play_sound(file_name: str):
    mixer.init()
    mixer.music.load(file_name)
    mixer.music.play()
    time.sleep(2)

#
# Notification Functions
#
def ping():
    sound_path = resources.files("meerkat") / "ping_sounds/default_ping.wav"
    _play_sound(str(sound_path))

def email(message="", token=None):
    if token == None:
        token = os.environ.get("MEERKAT_TOKEN")

    if not token:
        print("No MeerkatIO token found in the environment. Please login using `meerkat login` or go to https://meerkatio.com to set up your account to enable this feature.")
        return
    
    return send_meerkat_notification("email", token, message)

def sms(message="", token=None):
    if token == None:
        token = os.environ.get("MEERKAT_TOKEN")

    if not token:
        print("No MeerkatIO token found in the environment. Please login using `meerkat login` or go to https://meerkatio.com to set up your account to enable this feature.")
        return
    
    return send_meerkat_notification("sms", token, message)

def slack(message="", token=None):
    if token == None:
        token = os.environ.get("MEERKAT_TOKEN")

    if not token:
        print("No MeerkatIO token found in the environment. Please login using `meerkat login` or go to https://meerkatio.com to set up your account to enable this feature.")
        return
    
    return send_meerkat_notification("slack", token, message)

#
# iPython Extension
#

@magics_class
class MeerkatMagics(Magics):
    @line_magic
    def ping(self, line):
        sound_path = resources.files("meerkat") / "ping_sounds/default_ping.wav"
        _play_sound(str(sound_path))

    @line_magic
    def email(self, line):
        email(line)

    @line_magic
    def sms(self, line):
        sms(line)

    @line_magic
    def slack(self, line):
        slack(line)

try:
    # Register the magics with the notebook
    ip = get_ipython()
    ip.register_magics(MeerkatMagics)
except:
    # not in a notebook
    pass