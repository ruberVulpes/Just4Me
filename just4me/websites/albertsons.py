from selenium import webdriver
from selenium.webdriver.common.by import By

from just4me.websites import LoginElements, CouponElement, Authentication, TextInput
from just4me.websites.basesite import BaseSite


class Albertsons(BaseSite):
    site_name = "Albertsons"
    coupon_program_name = "just4U"
    home_url = "https://www.albertsons.com/"
    login_url = "https://www.albertsons.com/account/sign-in.html"
    login_elements = LoginElements("label-email", "label-password", "btnSignIn")

    coupon_element = CouponElement("grid-coupon-clip-button", "Clip Coupon")
    coupons_url = "https://www.albertsons.com/justforu/coupons-deals.html"
    continue_button_info = "load-more-container"

    post_login_element_info = "sign-in-profile-text"
    post_login_element_function = By.ID

    def __init__(
            self,
            browser: webdriver.Chrome,
            authentication: Authentication,
    ):
        self.continue_button_function = browser.find_element_by_class_name
        super().__init__(browser, authentication)

    def __get_to_login_page__(self) -> None:
        self.browser.get(self.login_url)
