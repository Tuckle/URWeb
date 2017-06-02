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

from URWeb.app.models.models import FriendsRequest
from URWeb.app.models.models import Location
from django.contrib.auth.models import User
from URWeb.app.models.models import Friends

class AcceptRequest(generic.View):

	def put(self, request, username):
		
		if not username:
			response = dict()
			return HttpResponse(json.dumps(response))
		else:
			
			data = json.loads(request.body)
			user = data['user']
			
			try:

				friendsList = Friends.objects.all().filter(username1 = username)
				actualFriends = set()
				for item in friendsList:
					actualFriends.add(item.username2)

				friendsList = Friends.objects.all().filter(username2 = username)			
				for item in friendsList:
					actualFriends.add(item.username1)
					
				if user in actualFriends:
					try:
						FriendsRequest.objects.all().filter(from_user = user).filter(to_user = username).delete()
						data = 'You are already friends. The request has been discarded!'
					except Exception as e:
						data = str(e)
					return HttpResponse(json.dumps(data))			

				friend = Friends(username1 = username, username2 = user)
				FriendsRequest.objects.all().filter(from_user = user).filter(to_user = username).delete()
				friend.save()
				data = "OK"

			except Exception as e:
				data = str(e)

			return HttpResponse(json.dumps(data))		
		
