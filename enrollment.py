import re

import pyautogui
import pyperclip
import time
import json
import time
import platform
from pynput import mouse, keyboard
import pyautogui

ACTIONS_FILE = "actions.json"
actions = []
recording = True
last_event_time = None   # <-- NEW: track last event time

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = False

import webbrowser

# url = "https://practiscore.com/tts-tactical-pistol-18feb2026/register"
# url = "https://practiscore.com/thunder-tactical-shooters-uspsa-match-21feb2026-clone/register"
# url = "https://practiscore.com/kidlat-shooters-march-uspsa-match-3-7-26/register"
# url = "https://practiscore.com/texas-state-open-championship-2026/register"
# url = "https://practiscore.com/texas-state-open-championship-2026/register"
# url = 


# email = "YourEmail@Address.com"
# email = "jimjywang@gmail.com"

# Determine modifier key (Ctrl on Windows/Linux, Command on macOS)
mod_key = "command" if platform.system() == "Darwin" else "ctrl"


def enable_windows_dpi_awareness():
    if platform.system() != "Windows":
        return
    try:
        import ctypes
        awareness = ctypes.c_int(2)
        ctypes.windll.shcore.SetProcessDpiAwareness(awareness)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

enable_windows_dpi_awareness()


INTERVAL_SHORT = 0.1
INTERVAL_LONG = 1.0


def enroll_by_email(
    first_name, 
    last_name,
    email,
    uspsa_member_number,
    url):

    # open webpage

    webbrowser.open(url)
    time.sleep(INTERVAL_LONG*2)


    # registration steps


    if 'thunder' in url:
        for i in range(17):
            pyautogui.press("tab")
            time.sleep(INTERVAL_SHORT)

        pyautogui.write(first_name, interval=INTERVAL_SHORT)
        time.sleep(INTERVAL_SHORT)
        pyautogui.press("tab")

        pyautogui.write(last_name, interval=INTERVAL_SHORT)
        time.sleep(INTERVAL_SHORT)
        pyautogui.press("tab")

        pyautogui.write(email, interval=INTERVAL_SHORT)
        time.sleep(INTERVAL_SHORT)


        # division and class        
        for i in range(2):
            pyautogui.press("tab")
            time.sleep(INTERVAL_SHORT)
            pyautogui.press("space")
            time.sleep(INTERVAL_SHORT)

        # categories
        for i in range(7):
            pyautogui.press("tab")
            time.sleep(INTERVAL_SHORT)

        # poower factor
        for i in range(1):
            pyautogui.press("tab")
            time.sleep(INTERVAL_SHORT)
            pyautogui.press("space")
            time.sleep(INTERVAL_SHORT)

        # membmer number
        pyautogui.press("tab")
        pyautogui.write(uspsa_member_number, interval=INTERVAL_SHORT)
        time.sleep(INTERVAL_SHORT)

        # officer and group
        for i in range(7):
            pyautogui.press("tab")
            time.sleep(INTERVAL_SHORT)

        pyautogui.press("tab")
        time.sleep(INTERVAL_SHORT)
        pyautogui.press("space")
        time.sleep(INTERVAL_SHORT)

        pyautogui.press("tab")
        time.sleep(INTERVAL_SHORT)
        pyautogui.press("space")
        time.sleep(INTERVAL_SHORT)

        time.sleep(INTERVAL_LONG*10)

        pyautogui.hotkey(mod_key, "w")



    if 'brazosland' in url:
        for i in range(17):
            pyautogui.press("tab")
            time.sleep(INTERVAL_SHORT)

        pyautogui.write(first_name, interval=INTERVAL_SHORT)
        time.sleep(INTERVAL_SHORT)
        pyautogui.press("tab")

        pyautogui.write(last_name, interval=INTERVAL_SHORT)
        time.sleep(INTERVAL_SHORT)
        pyautogui.press("tab")

        pyautogui.write(email, interval=INTERVAL_SHORT)
        time.sleep(INTERVAL_SHORT)
        pyautogui.press("tab")

        pyautogui.write(uspsa_member_number, interval=INTERVAL_SHORT)
        time.sleep(INTERVAL_SHORT)

        for i in range(9):
            pyautogui.press("tab")
            time.sleep(INTERVAL_SHORT)

        pyautogui.press("space")
        time.sleep(INTERVAL_SHORT)

        for i in range(2):
            pyautogui.press("tab")
            time.sleep(INTERVAL_SHORT)
            pyautogui.press("space")
            time.sleep(INTERVAL_SHORT)

        for i in range(2):
            pyautogui.press("tab")
            time.sleep(INTERVAL_LONG)

        pyautogui.press("space")
        time.sleep(INTERVAL_LONG)

        pyautogui.press("tab")
        time.sleep(INTERVAL_LONG)

        pyautogui.press("enter")

        time.sleep(INTERVAL_LONG*10)

        pyautogui.hotkey(mod_key, "w")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    enroll_by_email(
        first_name = "FirstName",
        last_name = "LastName",
        email = "jimjywang@gmail.com", 
        uspsa_member_number = "A170259", 
        url = "https://practiscore.com/thunder-tactical-shooters-uspsa-match-14mar2026/register",
        )
    

    # https://practiscore.com/kidlat-shooters-march-uspsa-match-3-7-26/register