from django.views.generic import View
from django.http import HttpResponse
import json
import jinja2
import os
import requests


class Plugin(View):
    RADIUS = 100
    LOCATION_DATA = {
        'lng': "151.1957362",
        'lat': "-33.8670522"
    }
    API_KEY = "AIzaSyDXYDYmpNXAo01aw71oMT6KJXoI1aTTyvg"
    PLACES_API_KEY = "AIzaSyCWAxJGAVwwJG4ugVA7BZX-1QHUQ2XwkVU"
    LANGUAGE = "en"
    LOCATION_TYPES = []
    STRING = ""

    def get(self, request):
        return HttpResponse('GET no result')

    def post(self, request):
        return HttpResponse('POST no result')

    def run(self, request_body, format):
        request_body = json.loads(request_body)

        if 'string' in request_body:
            self.STRING = request_body.get('string')

        if 'radius' in request_body:
            self.RADIUS = request_body.get('radius')
        if 'language' in request_body:
            self.LANGUAGE = request_body.get('language')
        if 'location_types' in request_body:
            self.LOCATION_TYPES = request_body.get('location_types')
        if 'location_data' in request_body:
            self.LOCATION_DATA = request_body.get('location_data')

        request_link = r'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={}&types={}&location={},{}&language={}&radius={}&key={}&strictbounds'.format(self.STRING, self.LOCATION_TYPES, 
            self.LOCATION_DATA['lat'], self.LOCATION_DATA['lng'], self.LANGUAGE, self.RADIUS, self.API_KEY)

        statuses = {
            'OK': ''
        }

        place_detail_link = r'https://maps.googleapis.com/maps/api/place/details/json?{}={}&key={}'
        html_data = []
        locations_ids = []
        # get request
        try:
            req = requests.get(request_link)
            if req:
                req = req.json()
                if 'predictions' in req and req['predictions']:
                    # html_data.extend(req['results'])
                    for item in req['predictions']:
                        if 'place_id' in item and item['place_id'] in locations_ids:
                            continue
                        item['place_details'] = {}

                        place_link = ''
                        if 'place_id' in item and item['place_id']:
                            locations_ids.append(item['place_id'])
                            place_link = place_detail_link.format('placeid', item['place_id'],
                                                                  self.PLACES_API_KEY)
                        if 'place_id' not in item and not item['place_id'] and 'reference' in item:
                            place_link = place_detail_link.format('reference', item['reference'],
                                                                  self.PLACES_API_KEY)
                        if place_link:
                            place_req = requests.get(place_link)
                            if place_req:
                                try:
                                    place_req = place_req.json()
                                    if 'result' in place_req:
                                        item['place_details'] = place_req['result']
                                except Exception:
                                    pass
                        html_data.append(item)
        except Exception as e:
            print("findNearbyPlacesExecption: " + str(e))
        path = r'URWeb\app\api\views\modules\{}\result_template.html'.format(os.path.basename(__file__)[:-3])
        j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(path)),
                                    trim_blocks=True)
        result_html = j2_env.get_template(os.path.basename(path)).render(html_data=html_data)
        return result_html
