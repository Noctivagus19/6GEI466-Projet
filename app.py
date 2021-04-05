from datetime import datetime

from flask import (
    Flask,
    render_template,
)

import json
import urllib3

app = Flask(__name__)


@app.template_filter()
def format_datetime(value):
    return datetime.fromtimestamp(value/1000.0).strftime('%Y-%m-%d at %H:%M:%S')


@app.route('/', methods=['GET'])
def index():
    http = urllib3.PoolManager()

    r = http.request('GET', '127.0.0.1:8080/api/v1/iss/astronauts')
    iss_astronauts = json.loads(r.data)

    r = http.request("GET", "127.0.0.1:8080/api/v1/iss/positions")
    iss_positions = json.loads(r.data)

    r = http.request("GET", "127.0.0.1:8080/api/v1/iss/pass-times")
    iss_pass_time = json.loads(r.data) if r.status == 200 else None

    return render_template(
        'accueil.html',
        positions=iss_positions,
        astros=iss_astronauts,
        pass_time=iss_pass_time,
    )


@app.route('/position/', methods=['GET'])
def geoloc():
    return render_template('position.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
