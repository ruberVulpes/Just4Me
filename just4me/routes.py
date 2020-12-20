from just4me import app


@app.route(rule='/home')
@app.route(rule='/')
def home():
    return 'Hello World'
