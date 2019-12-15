from collections import namedtuple
from os import getcwd, path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.wait import WebDriverWait

import env

TextInput = namedtuple("TextInput", ["id", "keys"])


def main():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(path.join(getcwd(), env.CHROME_DRIVER_DIR, env.CHROME_DRIVER), options=chrome_options)
    browser = login(browser)
    browser = just4you(browser)
    browser.quit()


def login(browser: webdriver.Chrome) -> webdriver.Chrome:
    text_inputs = [TextInput(env.email_text_entry_id, env.email),
                   TextInput(env.password_text_entry_id, env.password)]

    browser.get(env.VONS_LOG_IN_LINK)

    for text_input in text_inputs:
        element = browser.find_element_by_id(text_input.id)
        element.click()
        element.send_keys(text_input.keys)

    browser.find_element_by_id(env.sign_in_submit_id).click()
    print("Logged In")
    return browser


def just4you(browser: webdriver.Chrome) -> webdriver.Chrome:
    def is_add_button(button: WebElement) -> bool:
        return button.text == env.add_button_text and button.is_displayed()

    try:
        WebDriverWait(browser, 3).until(e_c.presence_of_element_located((By.ID, env.sign_in_button_id)))
        print("Home Page Loaded")
    except TimeoutException:
        print("Home Page Took Too Long")
        exit(1)
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
                print(f"Clicking Load More, clicked {buttons_clicked}")
            else:
                break
            load_more_button = browser.find_element_by_class_name(env.load_more_button_class)
    except NoSuchElementException:
        print("Finished adding all items")
        # Finished clicking all the deals
        pass
    except StaleElementReferenceException:
        env.MAX_REFRESHES -= 1
        if env.MAX_REFRESHES > 0:
            print("Stale Button, Refreshing")
            return just4you(browser)
    except ElementClickInterceptedException:
        env.MAX_REFRESHES -= 1
        if env.MAX_REFRESHES > 0:
            print("Click Intercepted, Refreshing")
            return just4you(browser)
    return browser


if __name__ == '__main__':
    main()
