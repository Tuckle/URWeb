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

class RejectRequest(generic.View):
	def get(self, request, username):
		if not username:
			response = dict()
			return HttpResponse(json.dumps(response))
		else:
			data = dict()
			return HttpResponse(json.dumps(data))

	def put(self, request, username):
		if not username:
			response = dict()
			return HttpResponse(json.dumps(response))
		else:
			data = dict()
			return HttpResponse(json.dumps(data))		
		
