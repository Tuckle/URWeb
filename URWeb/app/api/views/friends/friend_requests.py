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

class FriendRequests(generic.View):
	def get(self, request, username):
		if not username:
			response = dict()
			return HttpResponse(json.dumps(response))
		else:
			friendRequestsList = FriendsRequest.objects.all().filter(to_user = username)
			listI = list()
			for item in friendRequestsList:
				try:
					user_ = User.objects.get(username = item.from_user)					
					tt = {"name":user_.username, "email":user_.email}
					listI.append(tt)
				except:
					tt = {"name":from_user, "email":"No email"}
					listI.append(tt)

			data = dict()
			data['data'] = listI

			return HttpResponse(json.dumps(data))
