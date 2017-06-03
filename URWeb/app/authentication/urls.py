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
from django.conf.urls import url, include
#from .views.signup import SignupView
from .views.myaccount import MyAccountView
from .views.report import ReportView
from .views.help import HelpView
#from .views.forgotpassword import ForgotPasswordView
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import views as core_views

auth_urls = [
    #url(r'^login',  LoginView.as_view(template_name="login.html"), name='login'),
    url(r'^login',  auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout', auth_views.logout, {'template_name': 'logout.html', 'next_page': '/'}, name='logout'),
    #url(r'^logout', LogoutView.as_view(template_name="logout.html"), name='logout')
    #url(r'^signup', SignupView.as_view(template_name="signup.html"), name='signup'),
    url(r'^myaccount', MyAccountView.as_view(template_name='myaccount.html'), name='myaccount'), 
    url(r'^help', HelpView.as_view(template_name='help.html'), name='help'),
    url(r'^report', ReportView.as_view(template_name='report.html'), name='report'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password_reset/done', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^password_reset', auth_views.password_reset, name='password_reset'),
    url(r'^reset/done', auth_views.password_reset_complete, name='password_reset_complete'),    
    url(r'^signup', core_views.signup, name='signup'),
    #url(r'^forgotpassword', ForgotPasswordView.as_view(template_name="forgotpassword.html"), name='forgotpassword'),
]
