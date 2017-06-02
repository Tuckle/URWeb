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

class RejectRequest(generic.View):
	def put(self, request, username):
		if not username:
			response = dict()
			return HttpResponse(json.dumps(response))
		else:
			data = json.loads(request.body)
			user = data['user']
			print("Floricele2")
			try:
				FriendsRequest.objects.all().filter(from_user = user).filter(to_user = username).delete()
				data = "OK"
			except Exception as e:
				data = str(e)
			return HttpResponse(json.dumps(data))
		
