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

class SendFriendRequest(generic.View):

	def put(self, request, username):
		
		username = str(request.user)
		data = json.loads(request.body)
		email = data['email']

		if not username:
			response = dict()
			return HttpResponse(json.dumps(response))
		else:
			data = "Not ok"

			try:
				user = User.objects.get(email = email)

				friendsList = Friends.objects.all().filter(username1 = username)
				actualFriends = set()
				for item in friendsList:
					actualFriends.add(item.username2)

				friendsList = Friends.objects.all().filter(username2 = username)			
				for item in friendsList:
					actualFriends.add(item.username1)
				
				if user.username in actualFriends:
					data = 'You are already friends. The request has been discarded!'
					return HttpResponse(json.dumps(data))		

				if user.username == username:
					data = 'You canot be friend with yourself. The request has been discarded!'
					return HttpResponse(json.dumps(data))							

				currentFriendsRequest = FriendsRequest.objects.all().filter(from_user = username)
				for items in currentFriendsRequest:
					if user.username == items.to_user:
						data = 'You have already send a requests. The request has been discarded!'
						return HttpResponse(json.dumps(data))	

				friendRequest = FriendsRequest(from_user = username, to_user = user.username)
				friendRequest.save()
				data = "OK"

			except Exception as ex:
				data = str(ex)

			return HttpResponse(json.dumps(data))		
		
