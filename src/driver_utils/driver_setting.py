from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
def execute_folder():
    return os.path.dirname(os.path.abspath(__file__))

def get_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    #關掉不必要的message
    chrome_options.add_argument("--log-level=3")
    # 取得 driver_setting.py 的所在路徑
    current_file_dir = os.path.dirname(os.path.abspath(__file__))

    # 尋找 chromedriver.exe 的實際路徑
    driver_path = os.path.join(current_file_dir, "driver", "chromedriver.exe")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def take_screenshot(driver, prefix="screenshot"):
    try:
        screenshot_folder = os.path.join(execute_folder(), "screenshot")
        os.makedirs(screenshot_folder, exist_ok=True)

        timestamp = time.strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(screenshot_folder, f"{prefix}_{timestamp}.png")

        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
    except Exception as e:
        print(f"Error occurred in take_screenshot: {e}")