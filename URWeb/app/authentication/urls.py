"""URWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views.signup import SignupView
from .views.myaccount import MyAccountView
from .views.forgotpassword import ForgotPasswordView
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

auth_urls = [
    #url(r'^login',  LoginView.as_view(template_name="login.html"), name='login'),
    url(r'^login',  auth_views.login, {'template_name': 'login.html', "redirect_authenticated_user": True}, name='login'),
    url(r'^logout', auth_views.logout, {'template_name': 'logout.html', 'next_page': '/'}, name='logout'),
    #url(r'^logout', LogoutView.as_view(template_name="logout.html"), name='logout')
    url(r'^signup', SignupView.as_view(template_name="signup.html"), name='signup'),
    url(r'^myaccount', MyAccountView.as_view(template_name='myaccount.html'), name='myaccount'),
    url(r'^forgotpassword', ForgotPasswordView.as_view(template_name="forgotpassword.html"), name='forgotpassword'),
]
