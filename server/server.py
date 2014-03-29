from flask import Flask
from flask import jsonify
from flask import request


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hello/world/world')
def hello():
    return "This is the specific hello world"


# demonstrates flask debugging
@app.route('/bad')
def bad():
    x = 0
    y = 3
    return y / x


@app.route('/hello/<thing>')
def hello_thing(thing):
    result = "Hello %s" % str(thing)
    if request.args.get('bold', '0') != '0':
        result = "<b>%s</b>" % result
    return result


@app.route('/data')
def data():
    return jsonify({"some": "data"})


if __name__ == '__main__':
    debug_app = True
    app.run(debug=debug_app)
