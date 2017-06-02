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
		
		username = request.user
		data = json.loads(request.body)
		email = data['email']

		# tempUser = User(username = 'Gigi', firstname = 'Gheorghe', lastname = 'Balan', password = '00000000000000000000000000000000', email = 'gbalan@yahoo.com', pos_lat = '00,00', pos_lng = '00,00')
		# tempUser.save()
		# tempUser = User(username = 'Uli', firstname = 'Iulian', lastname = 'Bute', password = '00000000000000000000000000000001', email = 'ibute@yahoo.com', pos_lat = '00,00', pos_lng = '00,00')
		# tempUser.save()
		# tempUser = User(username = 'Adi', firstname = 'Adrian', lastname = 'Piriu', password = '00000000000000000000000000000002', email = 'apiriu@yahoo.com', pos_lat = '00,00', pos_lng = '00,00')
		# tempUser.save()
		# tempUser = User(username = 'PreaNesuferita', firstname = 'Ingrid', lastname = 'Stoleru', password = '00000000000000000000000000000003', email = 'istoleru@yahoo.com', pos_lat = '00,00', pos_lng = '00,00')
		# tempUser.save()



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
		
