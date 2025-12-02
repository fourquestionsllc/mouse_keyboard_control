import json
import time
from datetime import datetime
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

mouse = MouseController()
keyboard = KeyboardController()

def parse_button(button_str):
    # "Button.left" -> Button.left
    return getattr(Button, button_str.split('.')[-1])

def parse_key(key_str):
    # Normal characters: "a", "d", "g"
    # Special keys: "Key.enter"
    if key_str.startswith("Key."):
        return getattr(Key, key_str.split('.')[-1])
    else:
        return key_str  # single character

def replay_actions(path="input_record.json"):
    with open(path, "r") as f:
        events = json.load(f)

    # Sort by timestamp (IMPORTANT)
    events.sort(key=lambda e: e["time"])

    # Convert string times to datetime
    for e in events:
        e["time"] = datetime.fromisoformat(e["time"])

    # Replay
    print("Replaying recorded actions in 3 seconds...")
    time.sleep(3)

    for i, e in enumerate(events):
        if i > 0:
            delta = (e["time"] - events[i - 1]["time"]).total_seconds()
            if delta > 0:
                time.sleep(delta)

        etype = e["type"]

        # ------------------ Mouse Click ------------------
        if etype == "mouse_click":
            button = parse_button(e["button"])
            pressed = e["pressed"]
            x, y = e["position"]

            mouse.position = (x, y)

            if pressed:
                mouse.press(button)
            else:
                mouse.release(button)

        # ------------------ Mouse Scroll ------------------
        elif etype == "mouse_scroll":
            dx, dy = e["delta"]
            x, y = e["position"]
            mouse.position = (x, y)
            mouse.scroll(dx, dy)

        # ------------------ Key Press ---------------------
        elif etype == "key_press":
            key = parse_key(e["key"])
            keyboard.press(key)

        # ------------------ Key Release -------------------
        elif etype == "key_release":
            key = parse_key(e["key"])
            keyboard.release(key)

    print("Replay finished.")


if __name__ == "__main__":
    replay_actions("input_record.json")
