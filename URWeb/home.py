from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import redirect  
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import json
import tweepy
from django.conf import settings
from tweepy.parsers import Parser
from django.utils.datastructures import MultiValueDictKeyError


class HomeView(View):
    template_name = "home.html"
    
    def get(self, request, *args, **kwargs):

        #data = get_user_data(request)
        #data['username']
        return render_to_response('home.html', {'user': request.user, 'request': request})
        

   
def get_user_data(request):

        data = {}

        # create the connection
        auth = tweepy.OAuthHandler(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET)

        authUrl = auth.get_authorization_url()
	
        # set the token and verifier
        try:
            auth.request_token = (request.GET['oauth_token'], request.GET['oauth_verifier'])
        except MultiValueDictKeyError:
            data = None
        	
        # determine if we've already requested an access token
        if 'twitter_access_token_key' not in request.session:
  
        # get the access token
            try:
                access_token = auth.get_access_token(request.GET['oauth_verifier'])
                # update the stored values
                request.session['twitter_access_token_key'] = access_token.key
                request.session['twitter_access_token_secret'] = access_token.secret

            except MultiValueDictKeyError:
                data = None
        
        else:

            # set the access token
            auth.set_access_token(request.session['twitter_access_token_key'], request.session['twitter_access_token_secret'])

        # create the API instance
        api = tweepy.API(auth_handler=auth, parser=RawJsonParser)
        user = json.loads(api.me())

        # split the name
        full_name = user['name'].split(' ', 1)

        # get the user's info
        data['user_id'] = user['id']
        data['username'] = user['screen_name']
        data['full_name'] = user['name']
        data['first_name'] = full_name[0] if len(full_name) > 0 else ''
        data['last_name'] = full_name[1] if len(full_name) >= 2 else ''
        data['timezone'] = 0 if user['utc_offset'] is None else user['utc_offset'] / 3600
        data['picture'] = user['profile_image_url'].replace('_normal', '')

        return data