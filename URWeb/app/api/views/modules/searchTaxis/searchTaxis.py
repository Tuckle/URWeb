from django.views.generic import View
from django.http import HttpResponse
import json
import jinja2
import os
import requests
import time

class Plugin(View):
	RADIUS = 100
	LOCATION_DATA = {
		'lng': "151.1957362",
		'lat': "-33.8670522"
	}
	API_KEY = "AIzaSyDXYDYmpNXAo01aw71oMT6KJXoI1aTTyvg"
	PLACES_API_KEY = "AIzaSyCWAxJGAVwwJG4ugVA7BZX-1QHUQ2XwkVU"
	LANGUAGE = "en"
	OPEN_NOW = False

	def get_all(self, request_link):
		url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}" #  .format(googlePlacesResponse["next_page_token"], apiKey)
		next_page_token = None
		result = []
		current_time = time.time()
		while True:
			try:
				data = requests.get(request_link).json()
				if not data:
					raise Exception('Not found results')
				if "status" in data:
					if data['status'] not in ["OK", "ZERO_RESULTS"]:
						return []
				data_result = data.get('results', None)
				result.extend(data_result)
				next_page_token = data.get('next_page_token', None)
				request_link = url.format(next_page_token, self.API_KEY)
				current_time = time.time()
				if next_page_token is None:
					break
			except Exception as exception:
				new_time = time.time()
				if new_time - current_time > 3: 
					break
		return result

	def run(self, request_body, format):
		request_body = json.loads(request_body)

		if 'radius' in request_body:
			self.RADIUS = request_body.get('radius')
		if 'language' in request_body:
			self.LANGUAGE = request_body.get('language')
		if 'open_now' in request_body:
			self.OPEN_NOW = request_body.get('open_now')
		if 'location_data' in request_body:
			self.LOCATION_DATA = request_body.get('location_data')

		request_link = r'https://maps.googleapis.com/maps/api/place/nearbysearch/' \
					   r'json?location={},{}&radius={}&language={}&key={}&type=taxi_stand'.\
			format(self.LOCATION_DATA['lat'], self.LOCATION_DATA['lng'],
				   self.RADIUS, self.LANGUAGE, self.API_KEY)
		if self.OPEN_NOW:
			request_link += '&open' + 'now'

		request_link = request_link.format(' ').strip()

		statuses = {
			'OK': ''
		}

		result_set = self.get_all(request_link)

		place_detail_link = r'https://maps.googleapis.com/maps/api/place/details/json?{}={}&key={}'
		html_data = []
		locations_ids = []

		for item in result_set:
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

		path = r'URWeb\app\api\views\modules\{}\template.html'.format(os.path.basename(__file__)[:-3])
		j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(path)),
					trim_blocks=True)
		result_html = j2_env.get_template(os.path.basename(path)).render(html_data=html_data)
		return result_html
