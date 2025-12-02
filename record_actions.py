import json
from pynput import mouse, keyboard
from datetime import datetime

log = []
running = True  # shared flag


def now():
    return datetime.utcnow().isoformat()


# -------------------------
# Mouse Listeners
# -------------------------

def on_click(x, y, button, pressed):
    if not running:
        return False
    log.append({
        "type": "mouse_click",
        "button": str(button),
        "pressed": pressed,
        "position": (x, y),
        "time": now()
    })

def on_scroll(x, y, dx, dy):
    if not running:
        return False
    log.append({
        "type": "mouse_scroll",
        "delta": (dx, dy),
        "position": (x, y),
        "time": now()
    })

def on_move(x, y):
    if not running:
        return False
    # movement ignored
    return


# -------------------------
# Keyboard Listeners
# -------------------------

def on_press(key):
    global running

    if not running:
        return False

    try:
        k = key.char
    except:
        k = str(key)

    log.append({
        "type": "key_press",
        "key": k,
        "time": now()
    })


def on_release(key):
    global running

    try:
        k = key.char
    except:
        k = str(key)

    log.append({
        "type": "key_release",
        "key": k,
        "time": now()
    })

    # ESC stops EVERYTHING
    if key == keyboard.Key.esc:
        running = False
        return False  # stops keyboard listener


# -------------------------
# Main
# -------------------------

def main():
    print("Recording... Press ESC to stop.")

    mouse_listener = mouse.Listener(
        on_click=on_click,
        on_scroll=on_scroll,
        on_move=on_move
    )

    keyboard_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )

    mouse_listener.start()
    keyboard_listener.start()

    # Wait until ESC is pressed
    keyboard_listener.join()

    # Stop mouse listener manually
    mouse_listener.stop()

    # Save JSON
    with open("input_record.json", "w", encoding="utf-8") as f:
        json.dump(log, f, indent=4)

    print("Saved to input_record.json")


if __name__ == "__main__":
    main()
