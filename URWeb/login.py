from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import redirect  
from django.shortcuts import render_to_response

class LoginView(View):
    template_name = "login.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)            

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        if not username:
            return HttpResponse('Please input the username!')
        if not password:
            return HttpResponse('Please input the password!')  		
        if username!='Ana':
            return HttpResponse('Username not existing!')
        elif password!='orange':
            return HttpResponse('Wrong password!')
        else:
            redirect('/myaccount')
            return render_to_response('myaccount.html', {'name': request.POST['username']})
            
                
