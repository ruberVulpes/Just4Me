import logging.config

from flask import Flask

import env

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='')
app.config['SECRET_KEY'] = env.secret_key

logging.config.fileConfig(fname='logger.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from just4me import routes
