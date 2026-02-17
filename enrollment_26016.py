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

    webbrowser.open(url)
    time.sleep(INTERVAL_LONG*2)

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
        content_to_move_before_member_number = match1.group().strip()
        # print("Content before Member Number:", content_to_move_before_member_number)
    else:
        # print("No match for content before Member Number")
        content_to_move_before_member_number = None

    # 2️⃣ Content between Member Number and Waiver
    match2 = re.search(r'>\s*Member Number\s*<\s*(.*?)\s*>\s*Waiver\s*<small', clipboard_content, re.DOTALL)
    if match2:
        content_to_move_between_member_number_and_waiver = match2.group().strip()
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


    pyautogui.write(first_name, interval=INTERVAL_SHORT)

    pyautogui.press("tab")

    pyautogui.write(last_name, interval=INTERVAL_SHORT)

    pyautogui.press("tab")

    pyautogui.write(email, interval=INTERVAL_SHORT)


    content_to_move_html = [
        '>Division<',
        '>Power Factor<',
        '>Class<',
        'officer-certification" type="radio"',
        '>Phone</label>',
    ]



    checklist_to_skip = [
    'certification[]" type="checkbox"',
    'categories[]" type="checkbox"',
    'group_reg" type="checkbox"',
    '"group_reg_join" type="checkbox"',
    ]


    if content_to_move_before_member_number is not None:

        for c in content_to_move_html:
            if c in content_to_move_before_member_number:
                # print(f'processing {c}')
                pyautogui.press("tab")
                time.sleep(INTERVAL_SHORT)   
                pyautogui.press("space")
                time.sleep(INTERVAL_SHORT)   

        for cheklist_item in checklist_to_skip:
            for i in range(content_to_move_before_member_number.count(cheklist_item)):
                print(f'processing {cheklist_item}')
                pyautogui.press("tab")
                time.sleep(INTERVAL_SHORT)   
                pyautogui.press("space")
                time.sleep(INTERVAL_SHORT)   

            ## need to fill up a space

    # enter uspsa member
    pyautogui.press("tab")
    time.sleep(INTERVAL_SHORT)
    pyautogui.write(uspsa_member_number, interval=INTERVAL_SHORT)


    ###

    if content_to_move_between_member_number_and_waiver is not None:
        # ratio
        for c in content_to_move_html:
            if c in content_to_move_between_member_number_and_waiver:
                print(f'processing {c}')
                pyautogui.press("tab")
                time.sleep(INTERVAL_SHORT)   
                pyautogui.press("space")
                time.sleep(INTERVAL_SHORT)   

        for cheklist_item in checklist_to_skip:
            for i in range(content_to_move_between_member_number_and_waiver.count(cheklist_item)):
                print(f'processing {cheklist_item}')
                pyautogui.press("tab")
                time.sleep(INTERVAL_SHORT)   
                pyautogui.press("space")
                time.sleep(INTERVAL_SHORT)   


    # check waiver
    pyautogui.press("tab")
    time.sleep(INTERVAL_SHORT)
    pyautogui.press("space")

    # if 'Card Info' in  clipboard_content_original:

    # payment information 

    # content_to_move = [
    #     "_donation&quot;:0",
    #     "Click to apply the Junior (under 18) discount",
    # ]

    # for c in content_to_move:
    #     if c in clipboard_content:
    #         print(f'processing {c}')
    #         pyautogui.press("tab")
    #         time.sleep(INTERVAL_LONG)   

    # # enter card number
    # pyautogui.press("tab")
    # time.sleep(INTERVAL_LONG)

    # # enter payment link and select it 
    # pyautogui.press("tab")
    # time.sleep(INTERVAL_LONG)
    # pyautogui.press("space")
    # time.sleep(INTERVAL_LONG)

    # enter register
    pyautogui.press("tab")
    time.sleep(INTERVAL_LONG)

    pyautogui.press("space")
    time.sleep(INTERVAL_LONG*10)

    pyautogui.hotkey(mod_key, "w")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    enroll_by_email(
        first_name = "Yanlin",
        last_name = "Xiang",
        email = "yanlinxiang01@gmail.com", 
        uspsa_member_number = "A164967", 
        url = "https://practiscore.com/kidlat-shooters-march-uspsa-match-3-7-26/register",
        )
    

    # https://practiscore.com/kidlat-shooters-march-uspsa-match-3-7-26/register