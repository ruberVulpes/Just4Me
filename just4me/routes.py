from threading import Thread

import env
from just4me import app
from just4me import just4me
from just4me.websites import Authentication


@app.route(rule='/')
@app.route(rule='/home')
def home():
    return 'Hello World'


@app.route(rule='/vons')
@app.route(rule='/websites/vons')
def vons():
    authentication = Authentication(*env.vons_auth)
    Thread(target=just4me.vons, args=(authentication,)).start()
    return 'Running Vons Coupons with env.py'


@app.route(rule='/albertsons')
@app.route(rule='/websites/albertsons')
def albertsons():
    authentication = Authentication(*env.vons_auth)
    Thread(target=just4me.albertsons, args=(authentication,)).start()
    return 'Running Albertsons Coupons with env.py'
