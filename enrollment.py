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
url = "https://practiscore.com/bayou-city-monthly-may-10th-at-oilfield-sports-complex-1/register"
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

# -----------------------------
# RECORDING PART
# -----------------------------
def record_event(evt):
    """Attach timing info to event and store it."""
    global last_event_time

    now = time.time()
    if last_event_time is None:
        evt["delay"] = 0
    else:
        evt["delay"] = now - last_event_time

    last_event_time = now
    actions.append(evt)


def on_click(x, y, button, pressed):
    if pressed:
        btn = "left" if button == mouse.Button.left else "right"
        evt = {
            "type": "mouse_click",
            "button": btn,
            "position": [int(x), int(y)]
        }
        record_event(evt)
        print(f"Recorded mouse click: {btn} at {evt['position']}")


def on_key_press(key):
    try:
        k = key.char
    except AttributeError:
        k = f"Key.{key.name}"

    evt = {"type": "key_press", "key": k}
    record_event(evt)
    print(f"Recorded key press: {k}")



# -----------------------------
# REPLAY PART
# -----------------------------
def enroll_by_email(email):


    content_to_move = [
        "Division",
        "Junior",
        "Senior",
        "Super",
        "Distinguished",
        "Law",
        "Lady",
        "Lady",
        "Military",
        "Foreign",
        "Power Factor",
        "Class",
        "RM",
        "CRO",
        "RO",
        "ScoreKeeper",
        "None",
        "I would like to create a Group registration",
        "I have a group registration code",
    ]

    webbrowser.open(url)
    time.sleep(INTERVAL_LONG)

    mod_key = "ctrl"  # use "command" on Mac

    # # Select all
    # pyautogui.hotkey(mod_key, "a")
    # time.sleep(INTERVAL_SHORT)
    # pyautogui.hotkey(mod_key, "c")
    # time.sleep(INTERVAL_SHORT)    
    # clipboard_content_original = pyperclip.paste()
    # time.sleep(INTERVAL_LONG*2)


    # 1️⃣ Open page source (Ctrl+U)
    pyautogui.hotkey(mod_key, "u")
    time.sleep(INTERVAL_SHORT)  # wait for source code tab to open

    # 2️⃣ Select all (Ctrl+A) and copy (Ctrl+C)
    pyautogui.hotkey(mod_key, "a")
    time.sleep(INTERVAL_SHORT)
    pyautogui.hotkey(mod_key, "c")
    time.sleep(INTERVAL_LONG*2)

    # 3️⃣ Get content from clipboard
    clipboard_content = pyperclip.paste()
    # print("Copied content length:", len(clipboard_content))  # optional

    # 4️⃣ Close source tab (Ctrl+W)
    pyautogui.hotkey(mod_key, "w")


    # 1️⃣ Content between Email and Member Number
    match1 = re.search(r'>\s*Email\s*<\s*(.*?)\s*>\s*Member Number\s*<', clipboard_content, re.DOTALL)
    if match1:
        content_to_move_before_member_number = match1.group(1).strip()
        # print("Content before Member Number:", content_to_move_before_member_number)
    else:
        # print("No match for content before Member Number")
        content_to_move_before_member_number = None

    # 2️⃣ Content between Member Number and Waiver
    match2 = re.search(r'>\s*Member Number\s*<\s*(.*?)\s*>\s*Waiver\s*<', clipboard_content, re.DOTALL)
    if match2:
        content_to_move_between_member_number_and_waiver = match2.group(1).strip()
        # print("Content between Member Number and Waiver:", content_to_move_between_member_number_and_waiver)
    else:
        content_to_move_between_member_number_and_waiver = None
        # print("No match for content between Member Number and Waiver")


    initial_tabs = 17


    if 'Add<' in clipboard_content:
        initial_tabs += 1

    for i in range(initial_tabs):
        pyautogui.press("tab")
        time.sleep(INTERVAL_SHORT)


    pyautogui.write("FirstName", interval=INTERVAL_SHORT)

    pyautogui.press("tab")

    pyautogui.write("LastName", interval=INTERVAL_SHORT)

    pyautogui.press("tab")

    pyautogui.write(email, interval=INTERVAL_SHORT)


    content_to_move_html = [
        '>Division<',
        '>Power Factor<',
        '>Class<',
        'officer-certification" type="radio"',
        '>Phone<',
    ]

    for c in content_to_move_html:
        if c in content_to_move_before_member_number:
            # print(f'with {c}')
            pyautogui.press("tab")
            time.sleep(INTERVAL_SHORT)   
            pyautogui.press("space")
            time.sleep(INTERVAL_SHORT)   

    for i in range(content_to_move_before_member_number.count('type="checkbox"')):
        # print(f'with {c}')
        pyautogui.press("tab")
        time.sleep(INTERVAL_SHORT)   
        pyautogui.press("space")
        time.sleep(INTERVAL_SHORT)   


    pyautogui.press("tab")
    time.sleep(0.001)
    pyautogui.write("A123456", interval=INTERVAL_SHORT)


    if content_to_move_between_member_number_and_waiver is not None:
        # ratio
        for c in content_to_move_html:
            if c in content_to_move_between_member_number_and_waiver:
                # print(f'with {c}')
                pyautogui.press("tab")
                time.sleep(INTERVAL_SHORT)   
                pyautogui.press("space")
                time.sleep(INTERVAL_SHORT)   

        # check
        for i in range(content_to_move_between_member_number_and_waiver.count('type="checkbox"')):
            # print(f'with {c}')
            pyautogui.press("tab")
            time.sleep(INTERVAL_SHORT)   


        # check waiver
        pyautogui.press("tab")
        time.sleep(INTERVAL_SHORT)
        pyautogui.press("space")


    content_to_move = [
        "donation",
        "Click to apply the Junior (under 18) discount",
    ]

    for c in content_to_move:
        if c in clipboard_content:
            pyautogui.press("tab")
            time.sleep(INTERVAL_LONG)   

    # if 'Card Info' in  clipboard_content_original:


    if 'Stripe' in clipboard_content:

        # enter card number
        pyautogui.press("tab")
        time.sleep(INTERVAL_LONG)

        # enter payment link and select it 
        pyautogui.press("tab")
        time.sleep(INTERVAL_LONG)
        pyautogui.press("space")

    # enter register
    pyautogui.press("tab")
    time.sleep(INTERVAL_LONG)

    # pyautogui.press("space")
    time.sleep(INTERVAL_LONG*3)

    pyautogui.hotkey(mod_key, "w")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    for email in ["jimjywang@gmail.com", "crossdominantshooters@gmail.com"]:
        enroll_by_email(email)