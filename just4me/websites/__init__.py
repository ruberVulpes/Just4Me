from collections import namedtuple

LoginElements = namedtuple("LoginElements", ["email_entry_id", "password_entry_id", "sign_in_submit_id"])
CouponElement = namedtuple("CouponElements", ["coupon_button_class", "coupon_button_text"])
Authentication = namedtuple("Authentication", ["email", "password"])

TextInput = namedtuple("TextInput", ["element_id", "keys"])
