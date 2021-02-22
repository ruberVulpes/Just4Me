import logging
import time
from typing import Callable, List

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from just4me.websites import LoginElements, CouponElement, Authentication, TextInput

logger = logging.getLogger(__name__)


class BaseSite:
    site_name: str
    coupon_program_name: str
    home_url: str
    login_url: str
    coupons_url: str

    login_elements: LoginElements
    coupon_element: CouponElement

    post_login_element_info: str
    post_login_element_function: Callable

    continue_button_info: str
    continue_button_function: Callable

    authentication: Authentication

    browser: webdriver.Chrome

    total_coupons = 0
    times_load_more = 0
    load_more_log_frequency = 5

    time_out = 3
    max_retries = 5

    def __init__(
            self,
            browser: webdriver.Chrome,
            authentication: Authentication,
    ):
        self.browser = browser
        self.authentication = authentication

    def drive(self) -> None:
        self.login()
        time.sleep(2)
        self.go_to_coupon_site()
        time.sleep(2)
        self.click_coupons()
        while self.load_more():
            time.sleep(0.5)
            self.click_coupons()
        logger.info(f"Loaded More {self.times_load_more} times total for Site: {self.site_name}")
        logger.info(f"Clicked {self.total_coupons} total coupons on Site: {self.site_name}")
        self.browser.quit()

    def login(self) -> None:
        logger.info(f"Attempting to log into Site: {self.site_name}")
        self.__get_to_login_page__()
        text_inputs = [TextInput(self.login_elements.email_entry_id, self.authentication.email),
                       TextInput(self.login_elements.password_entry_id, self.authentication.password)]
        for text_input in text_inputs:
            element = self.browser.find_element_by_id(text_input.element_id)
            element.click()
            element.send_keys(text_input.keys)
        logger.info(f"Filled user info for Site: {self.site_name}")
        self.browser.find_element_by_id(self.login_elements.sign_in_submit_id).click()
        logger.info(f"Successfully Logged into Site: {self.site_name}")

    def __get_to_login_page__(self) -> None:
        raise NotImplemented

    def wait_for_site_load(self) -> bool:
        logger.info(f"Waiting for site load for Site: {self.site_name}")
        try:
            WebDriverWait(self.browser, self.time_out).until(expected_conditions.presence_of_element_located(
                (self.post_login_element_function, self.post_login_element_info)))
        except TimeoutException:
            logger.critical(f"Post login page took too long to load for Site: {self.site_name}")
            self.__quit_browser__()
            return False
        logger.info(f"Successfully loaded after log in for Site: {self.site_name}")
        return True

    def go_to_coupon_site(self) -> None:
        logger.info(f"Going to start program {self.coupon_program_name} on Site: {self.site_name}")
        self.browser.get(self.coupons_url)

    def click_coupons(self) -> None:

        def get_active_coupon_elements() -> List[WebElement]:
            def is_active_coupon_element(button: WebElement) -> bool:
                return button.is_displayed() and button.text == self.coupon_element.coupon_button_text

            coupon_elements = self.browser.find_elements_by_class_name(self.coupon_element.coupon_button_class)
            return [button for button in coupon_elements if is_active_coupon_element(button)]

        logger.debug(f"Clicking coupons on Site: {self.site_name}")
        coupons_clicked = 0
        active_coupon_elements = get_active_coupon_elements()
        try:
            for coupon_element in active_coupon_elements:
                coupon_element.click()
                coupons_clicked += 1
        except StaleElementReferenceException:
            self.__coupon_site_refresh__("StaleElementReference")
        except ElementClickInterceptedException:
            self.__coupon_site_refresh__("ElementClickIntercepted")
        self.total_coupons += coupons_clicked
        logger.debug(f"Clicked {coupons_clicked} coupons on Site: {self.site_name}")

    def load_more(self) -> bool:
        logger.debug(f"Attempting to load more on Site: {self.site_name}")
        try:
            load_element: WebElement = self.continue_button_function(self.continue_button_info)
            if load_element.is_displayed():
                load_element.click()
                logger.debug(f"Successfully loaded more on Site: {self.site_name}")
                self.times_load_more += 1
                self.__load_more_logger_helper__()
            else:
                logger.error(f"Load more button not displayed on Site: {self.site_name}")
            return True
        except NoSuchElementException:
            logger.warning(f"Failed to load more on Site: {self.site_name}")
            return False
        except AttributeError:
            necessary_attributes = ["continue_button_function", "continue_button_info"]
            logger.warning(f"Missing attributes needed  {' or '.join(necessary_attributes)} for Site: {self.site_name}")
            return False
        except StaleElementReferenceException:
            return self.__coupon_site_refresh__("StaleElementReference")
        except ElementClickInterceptedException:
            return self.__coupon_site_refresh__("ElementClickIntercepted")

    def __coupon_site_refresh__(self, reason: str) -> bool:

        def base_msg() -> str:
            return f"{self.coupons_url} for Site: {self.site_name} due to {reason}"

        self.max_retries -= 1
        if self.max_retries > 0:
            logger.warning(f"Refreshing {base_msg()}")
            self.browser.get(self.home_url)
            self.browser.get(self.coupons_url)
            return True
        logger.error(f"Max Retries hit for url: {base_msg()}")
        self.__quit_browser__()
        return False

    def __load_more_logger_helper__(self) -> None:
        if self.times_load_more % self.load_more_log_frequency == 0:
            logger.info(f"Loaded more {self.times_load_more} times for Site: {self.site_name}")

    def __quit_browser__(self) -> None:
        logger.info("Quitting Browser")
        self.browser.quit()
