import os

# region Selenium on Heroku
chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
chromedriver_bin = os.environ.get('GOOGLE_CHROME_BIN')
# endregion

token = os.environ['TOKEN']
env = os.environ.get('ENV', 'dev')
is_prod = env.lower() == 'prod'

# region Flask
secret_key = os.environ['SECRET_KEY']
# endregion
