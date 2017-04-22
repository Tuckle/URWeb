from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import redirect  
from django.shortcuts import render_to_response
from django.template.context import RequestContext

class HomeView(View):
    template_name = "home.html"
    
    def get(self, request, *args, **kwargs):
        return render_to_response('home.html', {'user': request.user, 'request': request})
        

   
