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
from URWeb.app.models.models import User
from URWeb.app.models.models import Friends

class SetLocation(generic.View):

	def put(self, request, username):
		
		if not username:
			response = dict()
			return HttpResponse(json.dumps(response))
		else:
			
			data = json.loads(request.body)
			location = data['location']
			
			for item in User.objects.all().filter(username = username):
			 	print(item.pos_lat, item.pos_timestamp)

			try:
				tempUser = User.objects.all().filter(username = username).update(pos_lat = location['lat'], pos_lng = location['lng'], pos_timestamp = datetime.now())	
				data = "OK"
			except Exception as e:
				data = str(e)


			
			for item in User.objects.all().filter(username = username):
			 	print(item.pos_lat, item.pos_timestamp)

			return HttpResponse(json.dumps(data))		
		
