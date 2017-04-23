from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.conf import settings
import requests

class Location(generic.TemplateView):
	template_name = "location.html"
