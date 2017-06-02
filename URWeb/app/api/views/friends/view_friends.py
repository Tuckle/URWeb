from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from URWeb.app.models.models import FriendsRequest
from URWeb.app.models.models import Location
from django.contrib.auth.models import User
from URWeb.app.models.models import Friends

import json
import re
import os
import pickle
import zipfile

class ViewFriends(generic.View):
	def get(self, request, username):
		if not username:
			response = dict()
			return HttpResponse(json.dumps(response))
		else:
			# objects = User.objects.all()
			# for items in objects:
			# 	print(items.username)
			# 	loc = Location.objects.all().filter(user_id = items.id)
			# 	for loc_item in loc:
			# 		print(loc_item.pos_timestamp)

			data = dict()
			# tempStuff = Friends.objects.all()
			# for items in tempStuff:
			# 	print(items.username1, items.username2)

			friendsList = Friends.objects.all().filter(username1 = username)
			actualFriends = set()
			for item in friendsList:
				actualFriends.add(item.username2)

			friendsList = Friends.objects.all().filter(username2 = username)			
			for item in friendsList:
				actualFriends.add(item.username1)
			
			listI = list()
			for item in actualFriends:
				try:
					user_ = User.objects.get(username = item)					
					tt = {"name":item, "email":user_.email}
					listI.append(tt)
				except:
					tt = {"name":item, "email":"No email."}
					listI.append(tt)
			data = dict()
			data['data'] = listI
			return HttpResponse(json.dumps(data))
