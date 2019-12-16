from selenium import webdriver
from selenium.webdriver.common.by import By

from websites.basesite import BaseSite, Authentication, LoginElements, CouponElement


class Vons(BaseSite):
    site_name = "Vons"
    coupon_program_name = "just4U"
    home_url = "https://www.vons.com/home.html"
    login_url = "https://www.vons.com/account/sign-in.html"
    login_elements = LoginElements("label-email", "label-password", "btnSignIn")

    coupon_element = CouponElement("grid-coupon-clip-button", "ADD")
    coupons_url = "https://www.vons.com/justforu/coupons-deals.html"
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
