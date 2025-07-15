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
    browser.add_cookie({"name": "MUSIC_U", "value": "0092F055425C76D0DBC620FFBF7E31493E58FEE462574A576BEDC54FD7DE6D1EECFDB0FD3BA7C52891E66FB220FF75D0C74BA5900A2862320E16AC173DBDD833C815E291C6804E55E8B419512744687C72A191A19B3E756C6B59BBB08B5DC0C686EF370157E81862D65F1B350AAE010D00B0F4706EA85C9D98D5263EDC3BB4AC208C0B87E7C606834AA70DFCE4B0DC28DB3DC44C5E66CB346ED60296461C07DB8EFB605D1FD09F31DDF6FC409EB4AC70856F07F0CB1BA05D33EA1449417311CFDF9C16F03D6B4B3CDB347B880DAF6795B150F46E9E524CC432486ED8C14F5D886FF09ED4E05338C4AE952C07D3BCA7CB5A8F51368C136DF1D28DE4FB63811B0BA2CC6A7D2D7321100056D652ACE07417B1DECCA487607DB132F327CF12F83953192C7B9032ABB01AC22489BECA2C2215ADEFD8E9FAC5E00648A8123929C80FBF8EB7A82919D1ABC7979EA72B28A5E7865B36E5B3196DCCD968565E3A3DDD4346EE"})
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
