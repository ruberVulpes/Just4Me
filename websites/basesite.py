import logging
from collections import namedtuple
from typing import Callable
from selenium import webdriver

LoginElements = namedtuple("LoginElements", ["email_entry_id", "password_entry_id", "sign_in_submit_id"])
CouponElement = namedtuple("CouponElements", ["coupon_button_class", "coupon_button_text"])
Authentication = namedtuple("Authentication", ["email", "password"])

TextInput = namedtuple("TextInput", ["element_id", "keys"])

logger = logging.getLogger(__name__)


class BaseSite:
    site_name: str
    coupon_program_name: str

    login_url: str
    coupons_url: str

    login_elements: LoginElements
    coupon_element: CouponElement

    continue_button_info: str
    continue_button_function: Callable

    authentication: Authentication

    browser: webdriver.Chrome

    def __init__(
            self,
            browser: webdriver.Chrome,
            authentication: Authentication,
    ):
        self.browser = browser
        self.authentication = authentication

    def drive(self) -> None:
        self.login()

    def login(self) -> None:
        logger.info(f"Attempting to log into Site: {self.site_name}")
        self.browser.get(self.login_url)
        text_inputs = [TextInput(self.login_elements.email_entry_id, self.authentication.email),
                       TextInput(self.login_elements.password_entry_id, self.authentication.password)]
        for text_input in text_inputs:
            element = self.browser.find_element_by_id(text_input.element_id)
            element.click()
            element.send_keys(text_input.keys)
        logger.info(f"Filled user info for Site: {self.site_name}")
        self.browser.find_element_by_id(self.login_elements.sign_in_submit_id).click()
        logger.info(f"Successfully Logged into Site: {self.site_name}")
