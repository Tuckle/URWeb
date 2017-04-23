from django.views.generic import View
from django.http import  HttpResponse


class Plugin(View):
    def get(self, request):
        return HttpResponse('GET no result')

    def post(self, request):
        return HttpResponse('POST no result')
