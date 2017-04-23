from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import redirect  

class ForgotPasswordView(View):
    template_name = "forgotpassword.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)            

    def post(self, request, *args, **kwargs):
        username  = request.POST['forgotpassword-username']
        old_password  = request.POST['old-password']
        new_password_1 = request.POST['new-password']
        new_password_2 = request.POST['check-new-password']

        if new_password_1!=new_password_2:
            return HttpResponse('The two new passwords must be the same!')
        else:
            return redirect('/myaccount')
                
