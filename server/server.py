import flask
from flask import Flask
from flask import request
import math
import cv2
import urllib
import focal_length
import radial_distortion


app = Flask(__name__, static_url_path='')

# stats for logit model
coeffs = [550.0269, 3.4448, 0.0003, 2.8752]


def calculate_distortion_score(image_url):
    rad = float(radial_distortion.main(image_url))

    (v0, o, h) = focal_length.compute_pp(image_url)
    f = float(focal_length.compute_focal_length(v0, o, h))

    # computer FOV
    img = cv2.imread(image_url, cv2.IMREAD_COLOR)
    h, w = img.shape[:2]
    FOV = float(focal_length.compute_fov(w, h, f))

    # predictive model
    b1 = math.exp(coeffs[0] * rad + coeffs[1] * FOV)
    b2 = math.exp(coeffs[2] * rad + coeffs[3] * FOV)

    p1 = b1 / (1 + b1 + b2)
    p2 = b2 / (1 + b1 + b2)

    score = p1 * 5 + p2 * 10

    return [rad, f, FOV, score]


@app.route('/')
def info():
    return "<h1>Scoring and Correcting Distorted Images</h1> \
    <h3>Tanay Mehta, Boris Treskunov, Grace Wang, Joseph Zhong</h3>"


@app.route('/get_image')
def get_edges_image():
    path = './vp_out/temp.jpg'
    resp = flask.make_response(open(path).read())
    resp.content_type = "image/jpeg"
    return resp



# TODO: change to query? ?q=
@app.route('/post/<path:image_url>')
def get_image(image_url):
    # return jsonify(url=image_url)

    temp_fname = 'temp.jpg'

    with open(temp_fname,'wb') as f:
        f.write(urllib.urlopen(image_url).read())

    # radial | focal length | FOV | overall
    scores = calculate_distortion_score(temp_fname)

    scores = [str(score) for score in scores]
    return ' '.join(scores)


@app.route('/hello/<thing>')
def hello_thing(thing):
    result = "Hello %s" % str(thing)
    if request.args.get('bold', '0') != '0':
        result = "<b>%s</b>" % result
    return result


if __name__ == '__main__':
    debug_app = True
    app.run(debug=debug_app)
