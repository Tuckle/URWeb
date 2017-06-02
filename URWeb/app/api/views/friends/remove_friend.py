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

class RemoveFriend(generic.View):

	def put(self, request, username):
		
		username = str(request.user)
						
		data = json.loads(request.body)
		user = data['user']

		if not username:
			response = dict()
			return HttpResponse(json.dumps(response))
		else:
			data = "Not ok"

			try:
				Friends.objects.all().filter(username1 = username).filter(username2 = user).delete()
				Friends.objects.all().filter(username1 = user).filter(username2 = username).delete()
				data = "OK"
			except Exception as ex:
				data = str(ex)

			return HttpResponse(json.dumps(data))		
		
