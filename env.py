import os

# region Vons
__vons_email__ = os.environ.get("vons_email")
__vons_password__ = os.environ.get("vons_password")
vons_auth = (__vons_email__, __vons_password__)
# endregion


# region Albertsons
# They're the same authentication
albertsons_auth = (__vons_email__, __vons_password__)
# endregion
