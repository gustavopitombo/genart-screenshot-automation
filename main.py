import time
import os
import threading
import itertools
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# URL to take screenshots
URL = "http://google.com" 

# path to save the screenshots
outputFolder = './output' 

# number of outputs to generate
editions = 256

# delay in seconds to wait for the page to load
delay = 3 

# Check if the path exists
isExist = os.path.exists(outputFolder)

# If not, create the path
if not isExist:
    os.makedirs(outputFolder)


def loading_animation(stop_event):
    spinner = itertools.cycle(["-", "\\", "|", "/"])
    while not stop_event.is_set():
        print(f"\rRunning {next(spinner)}", end="", flush=True)
        time.sleep(0.1)

    print("\rDone!     ", end="", flush=True) 

    
def genartScreenshot(eds=None):
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Helps in some environments
    options.add_argument("--disable-dev-shm-usage")  # Fixes some resource issues

    # Automatically download and set up the correct ChromeDriver
    service = Service(ChromeDriverManager().install())
    service.start()

    # Initialize Chrome browser
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_position(0, 0)

    # Set the window size, you can change the numbers to your desired size
    driver.set_window_size(1200, 1200)
    driver.get(URL)

    # Start loading animation in a separate thread
    stop_event = threading.Event()
    animation_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    animation_thread.start()

    # Wait for the page to load
    time.sleep(delay)

    take_screen_shot(driver, eds)

    # Stop animation
    stop_event.set()
    animation_thread.join()


def take_screen_shot(driver, eds):

    # Get the current edition
    current = editions - eds

    # Set the edition
    edition = eds - 1

    # Save a screenshot
    driver.save_screenshot(
        outputFolder + "/" + time.strftime("%Y%m%d") + "-" + str(current) + ".png")

    driver.quit()

    if edition > 0:
        genartScreenshot(edition)


genartScreenshot(editions)
