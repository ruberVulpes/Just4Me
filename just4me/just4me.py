from typing import Type

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from just4me.websites import Authentication
from just4me.websites.albertsons import Albertsons
from just4me.websites.basesite import BaseSite
from just4me.websites.vons import Vons


def albertsons(authentication: Authentication):
    _base_site(authentication, Albertsons)


def vons(authentication: Authentication):
    _base_site(authentication, Vons)


def _base_site(authentication: Authentication, site: Type[BaseSite]):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    site(browser, authentication=authentication).drive()
