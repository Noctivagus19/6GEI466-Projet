from flask import Flask, render_template
import json
import urllib3
import urllib
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

    return render_template(
        'accueil.html',
        issLon=longitude,
        issLat=latitude,
        astros=iss_astronauts,
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
