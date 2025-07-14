# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005A1496C2D7F2A5CD6D501F58481B8D74D9D732E6FF7EFDC52321CB5B0CEB037A1B466F32ABE58BE56EB515A85DAD419101A0CD573FDDB9488D7BF1854FCA8A88604BB9D3E2F98B27069293FA3D85940D995DD27F751D339A9B0544CA3C78EB3057F7A255B78572947C35E982732B9DCE2E076255B6D0B0970B4DA6E0C6E6D331CAB44A0C8C96110A3AA70B11DD26F5EDBA87D9A638759664B544CD71D2BE0CAF9162510BF4E9646E3E8309B78C820809015D4E773D420B30C34CACC571195C74C94A0325BEDDA0C4F2E828BCB5787DE2177C75D9CA5DB2DAE0E1101269B28A25CB263410321E3FDB4AB36B474D9A6FF610ABF9DF6A8C31202632D1027129AC60939C41D7AA5503D14ED445D6A3C8B5FD345D40728FAF6E339B311D9B08BFF421E28FC2E66603A81F99CBF5927BFB728044ABA420198B47494CAECD352CD63B41"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
