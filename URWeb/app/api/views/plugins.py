from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import json
import os
import pickle
                                
class Plugins(generic.View):

	pluginsPathList = r'URWeb\app\api\views\pluginsList'
	pluginsModulesPath = r'URWeb\app\api\views\modules'
	dictObject = None

	def saveDict(self):
		if self.dictObject:
			pFile = open(self.pluginsPathList, "wb")
			pickle.dump(self.dictObject, pFile)
			pFile.close()

	def loadDict(self):
		pFile = open(self.pluginsPathList, "rb")
		self.dictObject = pickle.load(pFile)
		pFile.close()
		
	def get(self, request, name, format):
		if not name:
			if not self.dictObject:
				self.loadDict()
			response = dict()
			response['data'] = self.dictObject
			return HttpResponse(json.dumps(response))
		else:
			data = dict()
			value = False
			if not self.dictObject:
				self.loadDict()
			for items in self.dictObject:
				if items['name'] == name:
					value = True
					path = items['path']
					break
			if value == False:
				data['result'] = False
				data['msg'] = 'The selected plugin could not be found'
			else:
				data['result'] = True
				pathToPlugin = os.path.join(self.pluginsModulesPath, path, path + ".html")
				file = open(pathToPlugin, "r")
				content = file.read()
				file.close()
				data['html'] = content
			return HttpResponse(json.dumps(data))

	def put(self, request, name, format):
		data = json.loads(request.body)
		if data['name'] == 'adi_plugin':
			return HttpResponse("OK")
		else:
			return HttpResponse("Bad plugin name")

	def post(self, request, name, format):
		if not name:
			data = json.loads(request.body)
			result = ''
		else:
			value = False
			if not self.dictObject:
				self.loadDict()
			for items in self.dictObject:
				if items['name'] == name:
					value = True
					path = items['path']
					break
			pathToPlugin = os.path.join(self.pluginsModulesPath, path, path + ".py")
			exec('from .modules.{}.{} import Plugin'.format(path, path))
			try:
				result = locals()
				exec("result = Plugin().run({})".format(request.body), globals(), result)
				print(result['result'])
			except Exception as e:
				print("No module named Main found\n{}".format(e))
			return HttpResponse("None")


