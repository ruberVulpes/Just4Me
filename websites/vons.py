from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from websites.basesite import BaseSite, Authentication, LoginElements, CouponElement


class Vons(BaseSite):
    site_name = "Vons"
    coupon_program_name = "just4U"

    login_url = "https://www.vons.com/account/sign-in.html"
    login_elements = LoginElements("label-email", "label-password", "btnSignIn")

    coupon_element = CouponElement("grid-coupon-clip-button", "ADD")
    coupons_url = "https://www.vons.com/justforu/coupons-deals.html"
    continue_button_info = "load-more-container"
    continue_button_function = WebDriver.find_element_by_class_name

    def __init__(
            self,
            browser: webdriver.Chrome,
            authentication: Authentication,
    ):
        super().__init__(browser, authentication)
