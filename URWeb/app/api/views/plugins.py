from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import json
import pickle
                                
class Plugins(generic.View):

	pluginsPath = r'URWeb\app\api\views\pluginsList'
	dictObject = None

	def saveDict(self):
		if self.dictObject:
			pFile = open(self.pluginsPath, "wb")
			pickle.dump(self.dictObject, pFile)
			pFile.close()

	def loadDict(self):
		pFile = open(self.pluginsPath, "rb")
		self.dictObject = pickle.load(pFile)
		pFile.close()
		
	def get(self, request, name, format):
		if not self.dictObject:
			self.loadDict()
		response = dict()
		response['data'] = self.dictObject
		return HttpResponse(json.dumps(response))

	def put(self, request, name, format):
		data = json.loads(request.body)
		if data['name'] == 'adi_plugin':
			return HttpResponse("OK")
		else:
			return HttpResponse("Bad plugin name")

	def post(self, request, name, format):
		data = json.loads(request.body)
		result = ''
		
