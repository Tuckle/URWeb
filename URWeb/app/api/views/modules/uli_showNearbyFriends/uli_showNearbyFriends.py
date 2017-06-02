from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
import json
import requests
import time

class Plugin():

	def constructData(self, googlePlacesResponse, apiKey, count = None):
		data = []
		resultCode = 0
		firstResultCode = 0
		counter = 0
		while True:
			if count != None:
				if counter >= count:
					break

			if "status" in googlePlacesResponse:
				if googlePlacesResponse['status'] == "OK":
					resultCode = -1
				elif googlePlacesResponse['status'] == "ZERO_RESULTS":
					resultCode = 0
				elif googlePlacesResponse['status'] == "OVER_QUERY_LIMIT":
					resultCode = 1
				elif googlePlacesResponse['status'] == "REQUEST_DENIED":
					resultCode = 2
				elif googlePlacesResponse['status'] == "INVALID_REQUEST":
					resultCode = 3
				else:
					resultCode = 4

				if counter == 0:
					firstResultCode = resultCode
				
				if resultCode == -1:
					if "results" in googlePlacesResponse:
						for result in googlePlacesResponse["results"]:
							data.append(result)

					if "next_page_token" in googlePlacesResponse:
						if len(googlePlacesResponse["next_page_token"]):
							url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}".format(googlePlacesResponse["next_page_token"], apiKey)
							currentTime = time.time()
							limitTime = currentTime + 10
							while limitTime < time.time():
								time.sleep(1)
								ret = requests.get(url)
								googlePlacesResponse = ret.json()
								if googlePlacesResponse['status'] == "OK":
									break
						else:
							break
					else:
						break
				else:
					break
			else:
				break
			counter += 1

		return firstResultCode, resultCode, data

	def processRequest(self, urlInput, apiKey, counter):
		response = requests.get(urlInput)
		response = response.json()
		firstResultCode, resultCode, data = self.constructData(response, apiKey, counter)

		allTypes = {}
		for x in data:
			for item in x['types']:
			# item = x['name']
				if item not in allTypes:
					allTypes[item] = 1
				else:
					allTypes[item] = allTypes[item] + 1

		"""<ul class="list-group">
  <li class="list-group-item">First item</li>
  <li class="list-group-item">Second item</li>
  <li class="list-group-item">Third item</li>
</ul>"""
		data = '''<ul class="list-group">'''
		for x in allTypes:
			data +=''' <li class="list-group-item">''' + str(x) + '''<span class="badge">''' + str(allTypes[x]) +'''</span></li>'''
		data += '''</ul>''' 
		return data

	def run(self, requestBody, format):
		apiKey = "AIzaSyDXYDYmpNXAo01aw71oMT6KJXoI1aTTyvg"
		data = json.loads(requestBody)
		vlat = "-33.8670522"
		vlng = "151.1957362"
		radius = 500
		if data['radius']:
			radius = data['radius']
		language = "en"
		if data['lng']:
			language = data['lng']
		open_now = False
		if data['open_now']:
			open_now = data['open_now']

		if data['ld']['lat']:
			vlat = data['ld']['lat']

		if data['ld']['lng']:
			vlng = data['ld']['lng']

		if open_now:
			url = r'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&language={}&opennow&key={}'.format(vlat, vlng, radius, language, apiKey)
		else:
			url = r'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&language={}&key={}'.format(vlat, vlng, radius, language, apiKey)
		data = self.processRequest(url, apiKey, 3)
		return data 