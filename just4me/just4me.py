from typing import Type

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import env
from just4me.websites import Authentication
from just4me.websites.albertsons import Albertsons
from just4me.websites.basesite import BaseSite
from just4me.websites.vons import Vons

chrome_options = webdriver.ChromeOptions()
if env.is_prod:
    chrome_options.binary_location = env.chromedriver_bin
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")


def albertsons(authentication: Authentication):
    _base_site(authentication, Albertsons)


def vons(authentication: Authentication):
    _base_site(authentication, Vons)


def _base_site(authentication: Authentication, site: Type[BaseSite]):
    if env.is_prod:
        browser = webdriver.Chrome(executable_path=env.chromedriver_path, options=chrome_options)
    else:
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    site(browser, authentication=authentication).drive()
