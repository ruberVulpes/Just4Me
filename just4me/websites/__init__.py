import logging
from collections import namedtuple

logger = logging.getLogger(__name__)

UserPass = namedtuple("UserPass", ["username", "password"])

from just4me.websites.basesite import BaseSite
from just4me.websites.vons import Vons
from just4me.websites.albertsons import Albertsons
