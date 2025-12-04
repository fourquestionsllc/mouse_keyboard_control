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


def start_recording():
    print("Recording mouse & keyboard with timing...")
    print("Press ESC to stop.\n")

    global recording

    def stop_on_esc(key):
        if key == keyboard.Key.esc:
            print("\nStopping recording...")
            global recording
            recording = False
            return False

    with mouse.Listener(on_click=on_click) as ml, \
         keyboard.Listener(on_press=on_key_press, on_release=stop_on_esc) as kl:
        while recording:
            time.sleep(0.05)

    with open(ACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(actions, f, indent=2)

    print(f"Saved {len(actions)} actions to {ACTIONS_FILE}")


# -----------------------------
# REPLAY PART
# -----------------------------
def replay_actions():
    with open(ACTIONS_FILE, "r", encoding="utf-8") as f:
        acts = json.load(f)

    print(f"Replaying {len(acts)} actions with original timing...")
    enable_windows_dpi_awareness()

    for event in acts:
        # Wait the recorded delay
        time.sleep(event.get("delay", 0))

        if event["type"] == "mouse_click":
            x, y = event["position"]
            pyautogui.moveTo(int(x), int(y))
            if event["button"] == "left":
                pyautogui.click()
            else:
                pyautogui.click(button="right")

        elif event["type"] == "key_press":
            k = event["key"]
            if k.startswith("Key."):
                key_name = k.split(".", 1)[1]
                special_map = {
                    "enter": "enter",
                    "space": "space",
                    "backspace": "backspace",
                    "tab": "tab",
                    "esc": "esc",
                    "shift": "shift",
                    "ctrl": "ctrl",
                    "alt": "alt",
                }
                mapped = special_map.get(key_name, key_name)
                try:
                    pyautogui.press(mapped)
                except Exception:
                    print(f"Warning: skipped unknown key {k}")
            else:
                pyautogui.typewrite(str(k))

    print("Replay complete.")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    mode = input("Type 'r' to record or 'p' to replay: ").strip().lower()

    if mode == "r":
        start_recording()
    elif mode == "p":
        replay_actions()
    else:
        print("Invalid option.")
