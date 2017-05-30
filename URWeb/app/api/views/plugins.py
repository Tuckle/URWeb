from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import json
import re
import os
import pickle
import zipfile
                                
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

	def refresh_plugin_list(plugin_name, plugin_description, plugin_path):
		self.loadDict()
		self.dictObject.append({
		    'name': plugin_name,
		    'description': plugin_description,
		    'path': plugin_path
		})
		self.saveDict()
		
		
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
		print(str(request.body))
		data = json.loads(request.body)

		print(str(data))
		
		file_path = os.path.join(self.pluginModulesPath, file_name)
		if not os.path.exists(file_path):
			os.makedirs(file_path)
		arc_handle = zipfile.ZipFile(arc_path, "r")
		arc_handle.extractall(file_path)
		arc_handle.close()

		# file checks
		pname_validation = re.match("^[\w]+.((zip)|(rar))$", data['name'])
		if not pname_validation:
			return HttpResponse("Bad plugin name")
		#if data['name'] == 'adi_plugin':
		#	return HttpResponse("OK")
		#else:
		#	return HttpResponse("Bad plugin name")
		# retrieve data about plugin to be uploaded(name, desc, path)
		file_name = None
		file_description = None
		arc_path = None #  archive path

		self.refresh_plugin_list(file_name, file_description, arc_path, file_path)

		return HttpResponse("OK")

	def post(self, request, name, format):
		if not name:
			data = json.loads(request.body)
			result = ''
		else:
			formatType = format
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
			result = ''
			try:
				result = locals()
				exec("result = Plugin().run({}, {})".format(request.body, formatType), globals(), result)
				result = result['result']
			except Exception as e:
				print("No module named Main found\n{}".format(e))
			return HttpResponse(result)


