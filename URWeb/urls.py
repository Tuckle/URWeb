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
from .home import HomeView
from .location import Location
from .beacon import Beacon
from .app.authentication.urls import auth_urls
from .app.api.urls import api_urls
from django.conf.urls.static import static

urlpatterns = [
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(template_name='home.html'), name='home'),
    url(r'^location', Location.as_view(), name='location'),
    url(r'^', include(auth_urls)),
    url(r'^api', include(api_urls)),
    url(r'^qr', include('qrauth.urls')),
    url(r'^beacon(?:/(?P<beacon_name>\d![a-zA-Z0-9]+))?', Beacon.as_view(), name='beacon'),
    # url(r'^\.well-known/', include('letsencrypt.urls')),
   ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
