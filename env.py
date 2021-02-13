import os

env = os.environ.get('ENV', 'dev')
is_prod = env.lower() == 'prod'

# region Selenium on Heroku
chromedriver_path = os.environ['CHROMEDRIVER_PATH']
chromedriver_bin = os.environ['GOOGLE_CHROME_BIN']
# endregion

token = os.environ['TOKEN']

# region Flask
secret_key = os.environ['SECRET_KEY']
# endregion
