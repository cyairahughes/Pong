import os, random, requests
from flask import Flask, jsonify
from requests.auth import HTTPDigestAuth
from flask_httpauth import HTTPDigestAuth as flaskauth

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = flaskauth()

default = {
    "vcu": "rams"
}


@app.route('/', methods=['GET'])
def index():
    url = 'http://127.0.0.1:5000/'
    r = requests.get(url + 'ping', auth=HTTPDigestAuth('vcu', 'rams'))
    return r.text, 201


@auth.get_password
def check_pw(usr):
    if usr in default:
        return default.get(usr)
    return None


@app.route('/pong', methods=['GET'])
@auth.login_required
def pong_get():
    return jsonify({'randomNum': random.randint(0, 10)}), 201


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'Page Not Here'}), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'message': 'Something is Broke'}), 500
