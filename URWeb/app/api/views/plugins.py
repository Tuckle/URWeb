from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from URWeb.app.models.models import Plugins as PluginDB

import json
import re
import os
import shutil
import pickle
import zipfile

class PluginConstants:
	PLUGIN_PATH_LIST = r'URWeb\app\api\views\pluginsList'
	PLUGINS_MODULES_PATH = r'URWeb\app\api\views\modules'
	PLUGINS_DOWNLOAD_PATH = r'URWeb\app\api\views\temp_downloads'
	TEMPLATE_DICT = {
		'name': '',
		'description': '',
		'path': ''
	}

	def load_plugins_list(self):
		with open(self.PLUGIN_PATH_LIST, "rb") as f:
			return pickle.load(f)

	def save_plugins_list(self, plugins_data):
		with open(self.PLUGIN_PATH_LIST, "wb") as f:
			pickle.dump(plugins_data, f)		                          	
	
                                
class Plugins(generic.View):

	pluginsPathList = r'URWeb\app\api\views\pluginsList'
	pluginsModulesPath = r'URWeb\app\api\views\modules'
	dictObject = None
	plugin_template = {
		'username': '',
		'name': '',
		'path': '',
		'description': ''
	}

	def saveDict(self):
		if self.dictObject:
			pFile = open(self.pluginsPathList, "wb")
			pickle.dump(self.dictObject, pFile)
			pFile.close()

	def loadDict(self):
		pFile = open(self.pluginsPathList, "rb")
		self.dictObject = pickle.load(pFile)
		pFile.close()

	def refresh_plugin_list(self, plugin_name, plugin_description, plugin_path):
		self.loadDict()
		self.dictObject.append({
		    'name': plugin_name,
		    'description': plugin_description,
		    'path': plugin_path
		})
		self.saveDict()
		
		
	def get(self, request, name, format):
		# self.loadDict()
		# PluginDB.objects.all().delete()
		# for item in self.dictObject:
		# 	new_plugin = PluginDB(username='admin', name=item['name'], path=item['path'], description=item['description'])
		# 	new_plugin.save()
			
		if not name:
			#if not self.dictObject:
			#	self.loadDict()
			#response = dict()
			#response['data'] = self.dictObject
			plugin_data = PluginDB.objects.all()			
			response = {
				'data': [
				{
				'username': item.username,
				'name': item.name,
				'path': item.path,
				'description': item.description
			} for item in plugin_data]}

			return HttpResponse(json.dumps(response))
		else:
			data = dict()
			#value = False
			#if not self.dictObject:
			#	self.loadDict()
			#for items in self.dictObject:
			#	if items['name'] == name:
			#		value = True
			#		path = items['path']
			#		break
			plugin_data = PluginDB.objects.all().filter(name=name)
			if not plugin_data:
				data['result'] = False
				data['msg'] = 'The selected plugin could not be found'
			else:
				data['result'] = True
				pathToPlugin = os.path.join(self.pluginsModulesPath, name, name + ".html")
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
			#for items in self.dictObject:
			#	if items['name'] == name:
			#		value = True
			#		path = items['path']
			#		break
			path = PluginDB.objects.all().filter(name=name).get('name')
			pathToPlugin = os.path.join(self.pluginsModulesPath, path, path + ".py")
			exec('from .modules.{}.{} import Plugin'.format(name, name))
			result = ''
			try:
				result = locals()
				exec("result = Plugin().run({}, {})".format(request.body, formatType), globals(), result)
				result = result['result']
			except Exception as e:
				print("No module named Main found\n{}".format(e))
		return HttpResponse(result)

	def delete(self, request, name, format):
		if not name:
			return HttpResponseNotFound('No plugin name given')
		try:
			username = str(request.user)
			data = PluginDB.objects.all().filter(name=name)
			if not data:
				return HttpResponseNotFound('Plugin name not found in database')
			data = data.filter(username=username)
			if not data and username != 'admin':
				return HttpResponseNotFound('User has no privileges to delete this plugin')
			path_to_plugin = os.path.join(self.pluginsModulesPath, name)
			try:
				shutil.rmtree(path_to_plugin)
			except Exception as e:
				print("Failed to remove plugin from modules folder")
			PluginDB.objects.all().filter(name=name).delete()
			
		except Exception as ex:
			print(str(ex))
			return HttpResponseNotFound(str(ex))
		return HttpResponse("OK")


class UploadPlugin(generic.View):
	PLUGIN_CONSTANTS = PluginConstants()
	ERROR = 'Failed to save file'

	def post(self, request, name):
		description = request.META.get('HTTP_DESCRIPTION')
		
		# check if plugin exists in db
		plugin_exists = PluginDB.objects.all().filter(name=name)
		
		if request.FILES and request.FILES.get('file_upload'):
			file_uploaded = self.save_and_process_file(name, description, request.FILES)
			if not file_uploaded:
				if not self.ERROR:
					self.ERROR = 'Failed to save file'
				return HttpResponse(self.ERROR)
		plugin_path = os.path.join(self.PLUGIN_CONSTANTS.PLUGINS_MODULES_PATH, name)
		new_plugin = PluginDB(username=str(request.user), name=name, path=plugin_path, description=description)
		new_plugin.save()
		return HttpResponse('OK')
	
	def unzip_file(self, file_path, to_dir):
		try:
			f = zipfile.ZipFile(file_path, "r")
			f.extractall(to_dir)
			f.close()
		except Exception as ex:
			print(str(ex))
			self.ERROR = str(ex)
			return False
		return True
	
	def download_file(self, file_data, to_path):
		if not os.path.exists(self.PLUGIN_CONSTANTS.PLUGINS_DOWNLOAD_PATH):
			os.makedirs(self.PLUGIN_CONSTANTS.PLUGINS_DOWNLOAD_PATH)
		try:
			with open(to_path, "wb+") as f:
				for chunk in file_data.chunks():
					f.write(chunk)				
		except Exception as ex:
			print(str(ex))
			self.ERROR = str(ex)
			return False
		return True

	def check_plugin(self, plugin_name):
		class_regex = re.compile('^class\s+Plugin\s*(\(|:).*$')
		func_regex = re.compile('^\s+def\s+run\s*\(\s*self.*$')

		path_to_plugin = os.path.join(self.PLUGIN_CONSTANTS.PLUGINS_MODULES_PATH, plugin_name)
		path_to_html = os.path.join(path_to_plugin, plugin_name + '.html')
		path_to_script = os.path.join(path_to_plugin, plugin_name + '.py')
		if not os.path.exists(path_to_html) or not os.path.exists(path_to_script):
			return False
		try:
			counter = 0
			found_class = False
			found_func = False
			with open(path_to_script) as f:
				for line in f:
					if re.match(class_regex, line):
						counter += 1	
					if re.match(func_regex, line):
						counter *= 2
				if counter != 2 or not found_class or not found_func:
					return False					
		except Exception as ex:
			print(str(ex))
			return False
		return True

	def add_plugin_to_list(self, plugin_name, plugin_path, description):
		plugins_data = self.PLUGIN_CONSTANTS.load_plugins_list()
		new_plugin = dict(PluginConstants.TEMPLATE_DICT)
		new_plugin['name'] = plugin_name
		new_plugin['description'] = description
		new_plugin['path'] = plugin_name
		plugins_data.append(new_plugin)
		self.PLUGIN_CONSTANTS.save_plugins_list(plugins_data)

	def save_and_process_file(self, plugin_name, plugin_description, file_dict):
		file_data = file_dict.get('file_upload')
		#plugin_name = file_dict.get('name')
		#plugin_description = file_dict.get('desc')

		fname, fext = os.path.splitext(file_data.name) 
		if not plugin_name:
			plugin_name = fname
		plugin_name = plugin_name.replace('[^\w]+', '_').replace('_+', '_')
		if not plugin_description:
			plugin_description = 'No description found for this plugin'

		zip_path = os.path.join(self.PLUGIN_CONSTANTS.PLUGINS_DOWNLOAD_PATH, file_data.name)
		if not self.download_file(file_data, zip_path):
			return False

		save_to = os.path.join(self.PLUGIN_CONSTANTS.PLUGINS_MODULES_PATH, plugin_name)
		if not self.unzip_file(zip_path, save_to):
			return False
		os.remove(zip_path)
		
#		if not self.check_plugin(plugin_name):
#			shutil.rmtree(save_to)
#			return False

		self.add_plugin_to_list(plugin_name, save_to, plugin_description)	

		return True