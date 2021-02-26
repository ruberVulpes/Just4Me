from contextlib import contextmanager
from typing import List

from selenium.webdriver.remote import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

from just4me.websites import UserPass


class BaseSite:
    site_name: str
    coupon_program_name: str
    total_coupons: int = 0
    times_load_more: int = 0

    def __init__(self, browser: webdriver.WebDriver, user_pass: UserPass):
        self.browser = browser
        self.user_pass = user_pass

    def drive(self):
        """
        This is the class that drives the coupon clicking for the website
        """
        raise NotImplementedError

    @contextmanager
    def _wait_for_page_load(self, timeout=3):
        """
        Context Manager for waiting for browser to load
        http://disq.us/p/x1r1v2
        :param timeout: The amount of time to wait for the html to grow stale
        """
        old_page = self.browser.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.browser, timeout).until(staleness_of(old_page))

    def _wait_for_element(self, locator_function: str, element: str, timeout=3) -> List[WebElement]:
        """
        Waits until element is located
        :param locator_function: The selenium.webdriver.common.by.By to look for
        :param element: The element's class/id/tag name to look or
        :param timeout: The amount of time to wait for the element to load

        """
        web_driver_wait = WebDriverWait(self.browser, timeout=timeout)
        return web_driver_wait.until(expected_conditions.presence_of_all_elements_located((locator_function, element)))
