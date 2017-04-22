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
from django.conf import settings
from django.contrib import admin
from URWeb.home import HomeView
from URWeb.login  import LoginView
from URWeb.logout import LogoutView
from URWeb.signup import SignupView
from URWeb.myaccount import MyAccountView
from URWeb.forgotpassword import ForgotPasswordView
from django.views.generic import TemplateView
from django.conf.urls.static import static

urlpatterns = [
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(template_name='home.html'), name='home'),
    url(r'^login',  LoginView.as_view(template_name="login.html"), name='login'),
    url(r'^signup', SignupView.as_view(template_name="signup.html"), name='signup'),		
    url(r'^myaccount', MyAccountView.as_view(template_name='myaccount.html'), name='myaccount'),
    url(r'^forgotpassword', ForgotPasswordView.as_view(template_name="forgotpassword.html"), name='forgotpassword'),
    url(r'^logout', LogoutView.as_view(template_name="logout.html"), name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
