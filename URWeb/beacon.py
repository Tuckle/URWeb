from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.conf import settings
import requests


class Beacon(generic.TemplateView):
    template_name = 'beacon.html'

    def post(self, request, beacon_name):
        beacon_name = '{}!{}'.format(request.POST['btype'], request.POST['bid'])
        link = 'https://proximitybeacon.googleapis.com/v1beta1/beacons/{}'.format(beacon_name)
        result_data = {}
        try:
            req = requests.get(link)
            req = req.json()
            if 'error' in req and 'message' in req['error']:
                result_data['error'] = req['error']['message']
            if 'beaconName' in req:
                result_data['beaconName'] = req['beaconName']
            if 'placeId' in req:
                result_data['placeId'] = req['placeId']
            if 'latLng' in req:
                result_data['latLng'] = "{},{}".format(req['latLng']['latitude'], req['latLng']['longitude'])
            if 'latLng' not in result_data:
                raise ValueError('Beacon location not found')
        except Exception as e:
            err_message = "Beacon not found: {}&nbsp;Exception occurred: {}".format(
                beacon_name, result_data['error'] if 'error' in result_data else str(e))
            print(err_message)
            return HttpResponseNotFound(err_message)
        # return HttpResponseRedirect('/location/{}'.format(result_data['latLng']))
        return HttpResponseRedirect('/location/')
