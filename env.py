from os import environ

# region Environment
CHROME_DRIVER = "win_chromedriver" if environ.get("env") == "windows" else "mac_chromedriver"
CHROME_DRIVER_DIR = "chromedriver"
# endregion

# region Authentication

# region Vons
__vons_email__ = environ.get("vons_email")
__vons_password__ = environ.get("vons_password")
vons_auth = (__vons_email__, __vons_password__)
# endregion

# endregion
