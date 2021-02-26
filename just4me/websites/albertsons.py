from selenium.webdriver.remote import webdriver

from just4me.websites import UserPass
from just4me.websites.vons import Vons


# Albertson's site is the same as Vons but just different urls
class Albertsons(Vons):
    site_name = "Albertsons"
    coupon_program_name = "just4U"

    home_url = 'https://www.albertsons.com/'
    login_url = 'https://www.albertsons.com/account/sign-in.html'
    coupons_url = 'https://www.albertsons.com/justforu/coupons-deals.html'
