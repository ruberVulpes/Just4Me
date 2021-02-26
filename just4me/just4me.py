from typing import Type

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import env
from just4me.websites import UserPass, Albertsons, Vons, BaseSite

chrome_options = webdriver.ChromeOptions()
if env.is_prod:
    chrome_options.binary_location = env.chromedriver_bin
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")


def albertsons(user_pass: UserPass):
    _website(user_pass, Albertsons)


def vons(user_pass: UserPass):
    _website(user_pass, Vons)


def _website(user_pass: UserPass, website: Type[BaseSite]):
    if env.is_prod:
        browser = webdriver.Chrome(executable_path=env.chromedriver_path, options=chrome_options)
    else:
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    website(browser, user_pass).drive()
