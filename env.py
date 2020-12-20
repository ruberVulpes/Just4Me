import os

# region Flask
secret_key = os.environ['SECRET_KEY']
# endregion

# region Vons
__vons_email__ = os.environ['vons_email']
__vons_password__ = os.environ['vons_password']
vons_auth = (__vons_email__, __vons_password__)
# endregion


# region Albertsons
# They're the same authentication
albertsons_auth = (__vons_email__, __vons_password__)
# endregion
