from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/')
def info():
    return "<h1>Scoring and Correcting Distorted Images</h1> \
    <h3>Tanay Mehta, Boris Treskunov, Grace Wang, Joseph Zhong</h3>"


@app.route('/post/<image_url>')
def get_image(image_url):
    return "Trying to undistort: %s" % image_url


@app.route('/hello/<thing>')
def hello_thing(thing):
    result = "Hello %s" % str(thing)
    if request.args.get('bold', '0') != '0':
        result = "<b>%s</b>" % result
    return result


if __name__ == '__main__':
    debug_app = True
    app.run(debug=debug_app)
