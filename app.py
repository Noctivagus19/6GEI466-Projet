from flask import Flask, render_template
import json
import urllib3

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    # http = urllib3.PoolManager()
    # r = http.request('GET', 'http://api.open-notify.org/iss-now.json')
    # obj = json.loads(r.data)
    # longitude = obj['iss_position']['longitude']
    # latitude = obj['iss_position']['latitude']

    return render_template('accueil.html')
