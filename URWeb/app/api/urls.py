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
from .views.plugins import Plugins, UploadPlugin
from .views.friends.view_friends import ViewFriends
from .views.friends.friend_requests import FriendRequests
from .views.friends.send_friend_request import SendFriendRequest
from .views.friends.accept_request import AcceptRequest
from .views.friends.reject_request import RejectRequest
from .views.friends.remove_friend import RemoveFriend
from .views.set_location import SetLocation

api_urls = [
    url(r'^/plugins(?:/(?P<name>\w+))?(?:/(?P<format>\w+))?$', Plugins.as_view(), name='plugins'),
    url(r'^/plugins/(?P<name>\w+)/upload/\w+', UploadPlugin.as_view(), name='upload_plugin'),
    url(r'^/friends/view(?:/(?P<username>\w+))?$', ViewFriends.as_view(),name = 'friends'),
    url(r'^/friends/friend_requests(?:/(?P<username>\w+))?$', FriendRequests.as_view(), name = 'friend_requests'),
    url(r'^/friends/send_request(?:/(?P<username>\w+))?$', SendFriendRequest.as_view(), name = 'send_request'),
    url(r'^/friends/reject_request(?:/(?P<username>\w+))?$', RejectRequest.as_view(), name = 'accept_request'),
    url(r'^/friends/accept_request(?:/(?P<username>\w+))?$', AcceptRequest.as_view(), name = 'reject_request'),
    url(r'^/friends/remove(?:/(?P<username>\w+))?$', RemoveFriend.as_view(), name = 'remove_friend'),
    url(r'^/set_location(?:/(?P<username>\w+))?$', SetLocation.as_view(), name = 'set_location')
]
