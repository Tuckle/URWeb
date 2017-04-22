from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import redirect  
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import json
import tweepy
from django.conf import settings
from tweepy.parsers import Parser
from django.utils.datastructures import MultiValueDictKeyError


class HomeView(View):
    template_name = "home.html"
    
    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name, {'user': request.user, 'request': request})
        

