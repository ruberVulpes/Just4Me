from os import environ

# region Environment
MAX_REFRESHES = 5
CHROME_DRIVER = "win_chromedriver" if environ.get("env") == "windows" else "mac_chromedriver"
CHROME_DRIVER_DIR = "chromedriver"
# endregion

# region Login Page
VONS_LOG_IN_LINK = "https://www.vons.com/account/sign-in.html"
email_text_entry_id = "label-email"
password_text_entry_id = "label-password"
sign_in_submit_id = "btnSignIn"
# endregion

# region Home Page
sign_in_button_id = "sign-in-profile-text"
# endregion

# region Just 4 U Page
VONS_JUST_4_U_Link = "https://www.vons.com/justforu/coupons-deals.html"
load_more_button_class = "load-more-container"
add_button_class = "grid-coupon-clip-button"
add_button_text = "ADD"
# endregion

# region Authentication
email = environ.get("email")
password = environ.get("password")
# endregion
