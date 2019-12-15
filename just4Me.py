import logging.config
from collections import namedtuple
from os import getcwd, path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

import env
from websites.basesite import Authentication
from websites.vons import Vons

TextInput = namedtuple("TextInput", ["id", "keys"])

logging.config.fileConfig(fname="logger.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def main():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(path.join(getcwd(), env.CHROME_DRIVER_DIR, env.CHROME_DRIVER), options=chrome_options)
    site = Vons(browser, authentication=Authentication(env.email, env.password))
    site.drive()
    while True:
        pass
    # browser = login(browser)
    # wait_for_home_load(browser)
    # browser = just4you(browser)
    # browser.quit()


def just4you(browser: webdriver.Chrome) -> webdriver.Chrome:
    logger.info("Starting Just4U")

    def is_add_button(button: WebElement) -> bool:
        return button.text == env.add_button_text and button.is_displayed()

    browser.get(env.VONS_JUST_4_U_Link)
    try:
        load_more_button = browser.find_element_by_class_name(env.load_more_button_class)
        while True:
            buttons_clicked = 0
            # Get All Add/Added Buttons on Page
            add_type_buttons = browser.find_elements_by_class_name(env.add_button_class)
            # Filter Buttons down to just Add Buttons
            add_buttons = [button for button in add_type_buttons if is_add_button(button)]
            for button in add_buttons:
                button.click()
                buttons_clicked += 1
            if load_more_button.is_displayed():
                load_more_button.click()
                logger.info(f"Clicking Load More, clicked {buttons_clicked}")
            else:
                break
            load_more_button = browser.find_element_by_class_name(env.load_more_button_class)
    except NoSuchElementException:
        logger.info("Finished adding all items")
        # Finished clicking all the deals
        pass
    except StaleElementReferenceException:
        env.MAX_REFRESHES -= 1
        if env.MAX_REFRESHES > 0:
            logger.warning("Stale Button, Refreshing")
            return just4you(browser)
        else:
            logger.error("Stale Button, Max Retries Hit")
    except ElementClickInterceptedException:
        env.MAX_REFRESHES -= 1
        if env.MAX_REFRESHES > 0:
            logger.warning("Click Intercepted, Refreshing")
            return just4you(browser)
        else:
            logger.error("Click Intercepted, Max Retries Hit")
    return browser


if __name__ == '__main__':
    logger.info("Starting Just4Me")
    main()
