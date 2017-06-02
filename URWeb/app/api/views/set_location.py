from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import json
import re
import os
import pickle
import zipfile
from datetime import datetime
from django.utils import timezone

from URWeb.app.models.models import FriendsRequest
from URWeb.app.models.models import Location
from django.contrib.auth.models import User
from URWeb.app.models.models import Friends

class SetLocation(generic.View):

	def put(self, request, username):
		
		username = request.user

		if not username:
			response = dict()
			return HttpResponse(json.dumps(response))
		else:
			
			data = json.loads(request.body)
			location = data['location']
			
			try:
				tempUser = User.objects.get(username = username)
				# print("UserId: {}".format(tempUser.id))
				updateLocation = Location.objects.all().filter(user_id = tempUser.id).update(pos_lat = location['lat'], pos_lng = location['lng'], pos_timestamp = datetime.now())	
				data = "OK"
			except Exception as e:
				data = str(e)

			# print("Data value: {}".format(data))
			
			for item in User.objects.all().filter(username = username):
				location = Location.objects.get(user_id = item.id)
				print(location.pos_lat, location.pos_lng, location.pos_timestamp)

			return HttpResponse(json.dumps(data))		
		
