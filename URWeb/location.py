from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.conf import settings
from django.shortcuts import redirect
from django.template.context import RequestContext
import requests
               
class Location(generic.TemplateView):

    template_name = "location.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect("/")        
        return render(request, self.template_name, {'request': request, 'user': request.user})

