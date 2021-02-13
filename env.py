import os

env = os.environ.get('ENV', 'dev')
is_prod = env.lower() == 'prod'

# region Selenium on Heroku
# https://stackoverflow.com/questions/48723397/how-to-set-path-to-chromedriver-in-heroku-chromedriver-buildpack/56648878
chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
chromedriver_bin = os.environ.get('GOOGLE_CHROME_BIN')
if is_prod:
    assert chromedriver_path is not None
    assert chromedriver_bin is not None
# endregion

token = os.environ['TOKEN']

# region Flask
secret_key = os.environ['SECRET_KEY']
# endregion
