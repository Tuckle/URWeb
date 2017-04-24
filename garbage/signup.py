from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import redirect  

class SignupView(View):
    template_name = "signup.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)            

    def post(self, request, *args, **kwargs):
        username  = request.POST['username']
        password  = request.POST['passwd']
        email     = request.POST['email']
        firstname = request.POST['firstname']
        lastname  = request.POST['lastname']

        redirect('/myaccount')
        return render(request, 'myaccount.html', {'name': request.POST['username']})                
