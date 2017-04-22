from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import redirect  
from django.shortcuts import render_to_response

class LogoutView(View):
    template_name = "logout.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)            

    def post(self, request, *args, **kwargs):
        username = None
        password = None
    
        return render_to_response('login.html', {'username': username}, {'password': password})
            
                
