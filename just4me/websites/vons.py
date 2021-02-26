from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webdriver

from just4me.websites import BaseSite, UserPass, logger


class Vons(BaseSite):
    site_name = 'Vons'
    coupon_program_name = 'Just4U'

    home_url = 'https://www.vons.com/home.html'
    login_url = 'https://www.vons.com/account/sign-in.html'
    coupons_url = 'https://www.vons.com/justforu/coupons-deals.html'

    load_more_class = 'load-more-container'

    def drive(self):
        # Failed to log in
        if not self._login():
            return self.browser.quit()

        self._go_to_coupon_site()
        # Wait for load more to appear before trying to click coupons
        self._wait_for_element(By.CLASS_NAME, self.load_more_class)

        self._click_coupons()
        # Click through paginated coupons
        while self._load_more():
            self._click_coupons()

        self.browser.quit()
        logger.info(f'Clicked coupons: {self.total_coupons}:{self.times_load_more} '
                    f'on site: {self.site_name} for user: {self.user_pass.username}')

    def _login(self) -> bool:
        login_element_ids = ('label-email', 'label-password')
        login_button_id = 'btnSignIn'

        # Get to login page and wait to load
        with self._wait_for_page_load():
            self.browser.get(self.login_url)

        # Fill login info
        for login_element_id, login_element_text in zip(login_element_ids, self.user_pass):
            login_element = self.browser.find_element_by_id(login_element_id)
            login_element.click()
            login_element.send_keys(login_element_text)

        # Login to site
        shared_log_fragment = f'site: {self.site_name} as user: {self.user_pass.username}'
        try:
            with self._wait_for_page_load():
                self.browser.find_element_by_id(login_button_id).click()
        except TimeoutException:
            logger.warning(f'Failed to log into {shared_log_fragment}')
            return False
        logger.info(f'Succeed in logging into {shared_log_fragment}')
        return True

    def _go_to_coupon_site(self):
        # Sometimes there will be a pop up about choosing a store
        # Close that pop up if it exists, even if it doesn't exist there's the same ID at 0, 0 😕
        close_popup_id = 'conflict-modal-close'
        if elements := self._wait_for_element(By.ID, close_popup_id):
            for element in elements:
                # Skip that 0, 0 element
                if element.location['x'] > 0 and element.location['y'] > 0:
                    ActionChains(self.browser).click(element).perform()

        # Navigate to the coupon site after closing the popup because closing the popup navigates home
        self.browser.get(self.coupons_url)

    def _click_coupons(self):
        coupon_button_text = 'Clip Coupon'
        coupon_button_class = 'grid-coupon-clip-button'

        try:
            # Get coupon elements to click
            coupon_elements = self._wait_for_element(By.CLASS_NAME, coupon_button_class)
        except TimeoutException:
            # No coupon elements found, but don't exit as there could be more coupons further down
            return

        # Click Coupons
        coupons_clicked = 0
        for coupon_element in coupon_elements:
            if coupon_element.text == coupon_button_text:
                ActionChains(self.browser).click(coupon_element).perform()
                coupons_clicked += 1

        self.total_coupons += coupons_clicked

    def _load_more(self) -> bool:
        try:
            load_more = self.browser.find_element_by_class_name(self.load_more_class)
        except NoSuchElementException:
            if self.times_load_more == 0:
                # Load more doesn't appear once coupons are exhausted
                # So only worry about not finding it if you've never clicked it
                logger.warning(f'Load More not found on Site: {self.site_name} for user: {self.user_pass.username}')
            return False

        ActionChains(self.browser).click(load_more).perform()
        self.times_load_more += 1
        return True
