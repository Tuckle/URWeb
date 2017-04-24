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
    LANGUAGE = "en"
    OPEN_NOW = False
    RANK_BY_PROMINENCE = False
    LOCATION_TYPES = []

    def get(self, request):
        return HttpResponse('GET no result')

    def post(self, request):
        return HttpResponse('POST no result')

    def run(self, request_body, format):
        request_body = json.loads(request_body)

        if 'radius' in request_body:
            self.RADIUS = request_body.get('radius')
        if 'language' in request_body:
            self.LANGUAGE = request_body.get('language')
        if 'open_now' in request_body:
            self.OPEN_NOW = request_body.get('open_now')
        if 'rank_by_prominence' in request_body:
            self.RANK_BY_PROMINENCE = request_body.get('rank_by_prominence')
        if 'location_types' in request_body:
            self.LOCATION_TYPES = request_body.get('location_types')
        if 'location_data' in request_body:
            self.LOCATION_DATA = request_body.get('location_data')

        request_link = r'https://maps.googleapis.com/maps/api/place/nearbysearch/' \
                       r'json?location={},{}&radius={}&language={}&key={}'.\
            format(self.LOCATION_DATA['lat'], self.LOCATION_DATA['lng'],
                   self.RADIUS, self.LANGUAGE, self.API_KEY)
        if self.OPEN_NOW:
            request_link += '&open' + 'now'

        request_link = request_link.format(' ').strip()

        request_link += '&type={}'
        statuses = {
            'OK': ''
        }

        html_data = []
        for type_ in self.LOCATION_TYPES:
            if not isinstance(type_, str):
                type_ = str(type_)
            req_copy = request_link.format(type_)

            # get request
            try:
                req = requests.get(req_copy)
                if req:
                    req = req.json()
                if 'results' in req:
                    html_data.extend(req['results'])
            except Exception as e:
                print("findNearbyPlacesExecption: " + str(e))
        path = r'URWeb\app\api\views\modules\{}\result_template.html'.format(os.path.basename(__file__)[:-3])
        j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(path)),
                                    trim_blocks=True)
        result_html = j2_env.get_template(os.path.basename(path)).render(html_data=html_data)
        print(result_html)
        return result_html
