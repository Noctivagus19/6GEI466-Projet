from flask import (
    Flask,
    render_template,
)

import json
import urllib3
import urllib
from urllib.parse import urlencode, quote_plus
from ip2geotools.databases.noncommercial import DbIpCity
from requests import get
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    http = urllib3.PoolManager()

    # Where is the ISS now
    r = http.request('GET', 'http://api.open-notify.org/iss-now.json')
    obj = json.loads(r.data)
    longitude = obj['iss_position']['longitude']
    latitude = obj['iss_position']['latitude']

    # ISS Pass times
    myIp = get('https://api.ipify.org').text
    infoIp = DbIpCity.get(myIp, api_key='free')
    myLocation = infoIp.city + ', ' + infoIp.region + ', ' + infoIp.country
    r = http.request('GET', 'http://api.open-notify.org/iss-pass.json?lat=' + str(infoIp.latitude) + '&lon=' + str(
        infoIp.longitude) + '')
    obj = json.loads(r.data)
    iss_risetimes = []
    for response in obj["response"]:
        print(response)
        iss_risetimes.append(datetime.fromtimestamp(response['risetime']))

    r = http.request('GET', '127.0.0.1:8080/api/v1/iss/astronauts')
    iss_astronauts = json.loads(r.data)

    return render_template(
        'accueil.html',
        issLon=longitude,
        issLat=latitude,
        astros=iss_astronauts,
        issRisetimes=iss_risetimes,
        infoLocation=myLocation
    )


@app.route('/position/', methods=['GET'])
def geoloc():
    return render_template('position.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
