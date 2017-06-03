from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
import json
import requests
import time
import math

from URWeb.app.models.models import FriendsRequest
from URWeb.app.models.models import Location
from django.contrib.auth.models import User
from URWeb.app.models.models import Friends
import datetime

class Plugin():
	def rad(self, value):
		return value * math.pi / 180

	def computeDistance(self,point1, point2):
		earthRadius = 6378137
		p2lat = float(point2.pos_lat)
		p2lng = float(point2.pos_lng)
		p1lat = float(point1.pos_lat)
		p1lng = float(point1.pos_lng)

		dLat = self.rad(p2lat - p1lat)
		dLng = self.rad(p2lng - p1lng)
		a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(self.rad(p1lat)) * math.cos(self.rad(p2lat)) * math.sin(dLng / 2) * math.sin(dLng / 2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		return earthRadius * c

	def getFriendsLocation(self, username, distance, deltaTime):
		my_id = User.objects.get(username = username)
		# myLocation = Location.objects.all().filter(user_id = my_id).update(pos_lat = "47.137132717193964", pos_lng="27.545814514160156", pos_timestamp = datetime.datetime.now())
		myLocation = Location.objects.get(user_id = my_id)
		
		friendsList = Friends.objects.all().filter(username1 = username)
		locationSet = set()
		actualFriends = set()
		for item in friendsList:
			actualFriends.add(item.username2)

		friendsList = Friends.objects.all().filter(username2 = username)			
		for item in friendsList:
			actualFriends.add(item.username1)

		for friend in actualFriends:
			user_id = User.objects.get(username = friend).id
			location = Location.objects.get(user_id = user_id)
			if self.friendIsNear(myLocation, location, distance, deltaTime):
				locationSet.add(location)
		locationSet.add(myLocation)
		return locationSet

	def friendIsNear(self, myLocation, friendLocation, distance, deltaTime):
		currentTime = datetime.datetime.now()
		friendStoredTime = datetime.datetime.strptime(str(friendLocation.pos_timestamp), "%Y-%m-%d %H:%M:%S.%f")
		myStoredTime = datetime.datetime.strptime(str(myLocation.pos_timestamp), "%Y-%m-%d %H:%M:%S.%f")

		if friendStoredTime + datetime.timedelta(minutes=int(deltaTime)) > currentTime and myStoredTime + datetime.timedelta(minutes=int(deltaTime)) > currentTime:
			if (self.computeDistance(myLocation, friendLocation) <= float(distance) * 1000):
				return True
		return False

	def constructData(self, locationSet):
		components = ""
		for item in locationSet:
			username = User.objects.get(id = item.user_id).username
			loc = "var temp_location = {lat: " + item.pos_lat +  " , lng: "+ item.pos_lng +  "}"
			components = components + """
			""" + loc + """
			addMarkerTer(temp_location, '"""+ username + """')
			"""
		script = """<script>console.log('ana')""" + components + """</script>"""
		return script


	def processRequest(self):
		return None


	def run(self, request_body, format):
		data = json.loads(request_body)
		distance = data['distance']
		deltaTime = data['deltaTime']
		username = data['username']
		locationSet = self.getFriendsLocation(username, distance, deltaTime)
		data = self.constructData(locationSet)
		return data 