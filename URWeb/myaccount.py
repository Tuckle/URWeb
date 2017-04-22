from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.views import View
from django.shortcuts import redirect
from django.template.context import RequestContext
import tweepy

class MyAccountView(View):
    template_name = "myaccount.html"
      
    def get(self, request, *args, **kwargs):
        
        return render_to_response(self.template_name, {'request': request, 'user': request.user})
