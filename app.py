import logging.config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from websites.vons import Vons
from websites.basesite import Authentication

import env

logging.config.fileConfig(fname='logger.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    vons = Vons(browser, authentication=Authentication(*env.vons_auth))
    vons.drive()


if __name__ == '__main__':
    logger.info('Starting Just4Me')
    main()
