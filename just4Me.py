import logging.config
from collections import namedtuple
from os import getcwd, path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    site = Vons(browser, authentication=Authentication(*env.vons_auth))
    site.drive()


if __name__ == '__main__':
    logger.info("Starting Just4Me")
    main()
