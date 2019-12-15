import logging
from collections import namedtuple
from typing import Callable, List
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

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

    post_login_element_info: str
    post_login_element_function: Callable

    time_out: int

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
        self.wait_for_site_load()
        self.click_coupons()

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

    def wait_for_site_load(self) -> None:
        logger.info(f"Waiting for site load for Site: {self.site_name}")
        try:
            WebDriverWait(self.browser, self.time_out).until(expected_conditions.presence_of_element_located(
                (self.post_login_element_function, self.post_login_element_info)))
        except TimeoutException:
            logger.critical(f"Post login page took too long to load for Site: {self.site_name}")
            raise TimeoutException
        logger.info(f"Successfully loaded after log for Site: {self.site_name}")

    def click_coupons(self):

        def get_active_coupon_elements() -> List[WebElement]:
            def is_active_coupon_element(button: WebElement) -> bool:
                return button.is_displayed() and button.text == self.coupon_element.coupon_button_text

            coupon_elements = self.browser.find_elements_by_class_name(self.coupon_element.coupon_button_class)
            return [button for button in coupon_elements if is_active_coupon_element(button)]

        logger.info(f"Clicking coupons on Site: {self.site_name}")
        coupons_clicked = 0
        self.browser.get(self.coupons_url)
        active_coupon_elements = get_active_coupon_elements()
        for coupon_element in active_coupon_elements:
            coupon_element.click()
            coupons_clicked += 1
        logger.info(f"Clicked {coupons_clicked} coupons on Site: {self.site_name}")
