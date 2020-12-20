import logging.config

from flask import Flask

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = ''

logging.config.fileConfig(fname='logger.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from just4me import routes
