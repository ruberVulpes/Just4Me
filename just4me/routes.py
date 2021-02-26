from threading import Thread

from flask import render_template, redirect, flash, url_for, make_response

import env
from just4me import app
from just4me import just4me
from just4me import logger
from just4me.forms import CouponWebsiteLoginForm
from just4me.websites import UserPass


@app.route(rule='/')
def index():
    return render_template('index.html')


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
            logger.info(f'Clicking coupons on {website} for {form.email.data}')
            Thread(target=target, args=(UserPass(form.email.data, form.password.data),)).start()
            flash(f"We're clicking your coupons for {website.title()}", 'success')
            return redirect(url_for('index'))
        flash('Invalid Token', 'danger')
    return render_template('coupon_website.html', title=website.title(), form=form)
