from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Launch Chrome
# driver = webdriver.Chrome()

chrome_options = Options()

# Use your existing Chrome profile
chrome_options.add_argument(r"--user-data-dir=C:\Users\yanli\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument(r"--profile-directory=Default")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://practiscore.com/tts-tactical-pistol-18feb2026/register")

time.sleep(5)  # wait for page to load

# How many TABs to simulate
num_tabs = 20

for i in range(num_tabs):
    # Get currently focused element
    active = driver.switch_to.active_element

    tag = active.tag_name
    input_type = active.get_attribute("type")
    name = active.get_attribute("name")
    id_attr = active.get_attribute("id")
    value = active.get_attribute("value")
    placeholder = active.get_attribute("placeholder")
    text = active.text.strip()
    checked = active.get_attribute("checked")

    # Only show if it's a text input, textarea, checkbox, or button
    if tag == "textarea" or tag == "button" or (tag == "input" and input_type in ["text", "email", "password", "checkbox", "submit"]):
        print(f"\nFocus #{i+1}")
        print("Tag:", tag)
        print("Type:", input_type if input_type else "None")
        print("Name:", name if name else "None")
        print("ID:", id_attr if id_attr else "None")
        print("Text:", text if text else "None")
        print("Value:", value if value else "None")
        print("Placeholder:", placeholder if placeholder else "None")
        print("Checked:", "Yes" if checked else "No")

    # Press TAB to move to the next element
    active.send_keys(Keys.TAB)
    time.sleep(0.3)  # allow focus to move
