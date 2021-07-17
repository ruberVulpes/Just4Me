import os

from just4me.just4me import vons, albertsons
from just4me.websites import UserPass

if __name__ == '__main__':
    albertsons(UserPass(os.getenv('email'), os.getenv('password')))
