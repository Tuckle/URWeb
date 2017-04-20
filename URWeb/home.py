from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.conf import settings


class Login(generic.TemplateView):
    template_name = "login.html"

                                
class MyAccount(generic.TemplateView):
    template_name = "myaccount.html"


class SignUp(generic.TemplateView):
    template_name = "signup.html"

class ForgotPassword(generic.TemplateView):
    template_name = "forgotpassword.html"

class Logout(generic.TemplateView):
    template_name = "logout.html"


class Home(generic.TemplateView):
    template_name = "home.html"

