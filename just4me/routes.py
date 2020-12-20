from threading import Thread

from flask import render_template, redirect, flash, url_for, make_response

import env
from just4me import app
from just4me import just4me
from just4me.forms import CouponWebsiteLoginForm
from just4me.websites import Authentication


@app.route(rule='/')
@app.route(rule='/home')
def home():
    return render_template('home.html')


@app.route(rule='/websites/<website>', methods=['GET', 'POST'])
def coupon_websites(website: str):
    if website.lower() == 'vons':
        target = just4me.vons
    elif website.lower() == 'albertsons':
        target = just4me.albertsons
    else:
        return make_response('', 404)
    form = CouponWebsiteLoginForm()
    if form.validate_on_submit():
        if form.token.data == env.token:
            Thread(target=target, args=(Authentication(form.email.data, form.password.data),)).start()
            flash(f"We're clicking your coupons for {website}", 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid Token', 'danger')
    return render_template('coupon_website.html', title=website.title(), form=form)
