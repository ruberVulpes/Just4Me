from collections import namedtuple
from typing import Callable
from selenium import webdriver

LoginElements = namedtuple("LoginElements", ["email_entry_id", "password_entry_id", "sign_in_submit_id"])
CouponElement = namedtuple("CouponElements", ["coupon_button_class", "coupon_button_text"])
Authentication = namedtuple("Authentication", ["email", "password"])


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
            browser: webdriver.chrome,
            authentication: Authentication,
            login_elements: LoginElements,
            login_url: str,
            coupon_element: CouponElement,
            coupons_url: str,
            continue_button="",
            continue_button_function=Callable,
            site_name="",
            coupon_program_name="",
    ):
        self.browser = browser
        self.authentication = authentication
        self.login_elements = login_elements
        self.login_url = login_url
        self.coupon_element = coupon_element
        self.coupons_url = coupons_url
        self.continue_button = continue_button
        self.continue_button_function = continue_button_function
        self.site_name = site_name
        self.coupon_program_name = coupon_program_name
