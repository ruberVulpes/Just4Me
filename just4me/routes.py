from threading import Thread
from flask import render_template, url_for
import env
from just4me import app
from just4me import just4me
from just4me.websites import Authentication


@app.route(rule='/')
@app.route(rule='/home')
def home():
    return render_template('home.html')


@app.route(rule='/vons')
@app.route(rule='/websites/vons')
def vons():
    authentication = Authentication(*env.vons_auth)
    Thread(target=just4me.vons, args=(authentication,)).start()
    return render_template('vons.html', title='Vons')


@app.route(rule='/albertsons')
@app.route(rule='/websites/albertsons')
def albertsons():
    authentication = Authentication(*env.vons_auth)
    Thread(target=just4me.albertsons, args=(authentication,)).start()
    return render_template('albertsons.html', title='Albertsons')
