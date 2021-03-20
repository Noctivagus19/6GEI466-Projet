from flask import Flask, render_template
import json
import urllib3
import urllib
from ip2geotools.databases.noncommercial import DbIpCity
from requests import get
from datetime import datetime
from urllib.parse import urlencode, quote_plus

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    http = urllib3.PoolManager()

    # Where is the ISS now
    r = http.request('GET', 'http://api.open-notify.org/iss-now.json')
    obj = json.loads(r.data)
    longitude = obj['iss_position']['longitude']
    latitude = obj['iss_position']['latitude']

    # Who are in space right now
    r = http.request('GET', 'http://api.open-notify.org/astros.json')
    obj = json.loads(r.data)
    iss_astronauts = []
    for astro in obj["people"]:
        if astro["craft"] == 'ISS':
            astro['wiki_page'] = search_wikipedia(astro['name'])
            iss_astronauts.append(astro)

    # ISS Pass times
    myIp = get('https://api.ipify.org').text
    infoIp = DbIpCity.get(myIp, api_key='free')
    myLocation = infoIp.city + ', ' + infoIp.region + ', ' + infoIp.country
    r = http.request('GET', 'http://api.open-notify.org/iss-pass.json?lat='+str(infoIp.latitude)+'&lon='+str(infoIp.longitude)+'')
    obj = json.loads(r.data)
    iss_risetimes = []
    for response in obj["response"]:
        print(response)
        iss_risetimes.append(datetime.fromtimestamp(response['risetime']))

    return render_template(
        'accueil.html',
        issLon=longitude,
        issLat=latitude,
        astros=iss_astronauts,
        issRisetimes=iss_risetimes,
        infoLocation=myLocation
    )


def search_wikipedia(term):
    http = urllib3.PoolManager()
    payload = {
        'action': 'query',
        'list': 'search',
        'prop': 'pageimages',
        'srsearch': f'{term} astronaut',
        'format': 'json',
    }
    payload = urlencode(payload, quote_via=urllib.parse.quote)
    wiki_url = 'http://en.wikipedia.org/'
    link = f'{wiki_url}w/api.php?{payload}'
    r = http.request('GET', link)
    obj = json.loads(r.data)

    wiki_page = {}

    if len(obj['query']['search']) > 0:
        first_result = obj['query']['search'][0]
        page_title = str.replace(first_result['title'], ' ', '_')
        wiki_page['url'] = f'https://en.wikipedia.org/wiki/{page_title}'
        wiki_page['snippet'] = first_result['snippet']

    return wiki_page

@app.route('/position/', methods=['GET'])
def geoloc():
    return render_template('position.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
