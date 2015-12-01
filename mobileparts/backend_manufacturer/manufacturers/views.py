from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import logging
from manufacturers.models import Manufacturer
import json
import requests
import os
from django.conf import settings

@csrf_exempt
def list(request):
	if request.method == "GET":
		manufacturers = Manufacturer.objects.all()
		results = [ob.as_json() for ob in manufacturers]
		result = {"count": Manufacturer.objects.count(), "manufacturers": results}
		return HttpResponse(json.dumps(result))
	return HttpResponse("Ok")

def list_num(request, manufacturer_id):
	if request.method == "GET":
		logger = logging.getLogger('backend_device')
		try:
			manufacturer = Manufacturer.objects.get(manufacturer_id)
			results = manufacturer.as_json()
			result = {"manufacturer": results}
			data = json.dumps(result)
			logger.info(data)
			return HttpResponse(data)
		except ObjectDoesNotExist:
			data = json.dumps({"manufacturer": 0})
			logger.info(data)
			return HttpResponse(json.dumps(result), status=404)
	return HttpResponse("Ok")

@csrf_exempt
def remove(request):
	if request.method == "POST":
		logger = logging.getLogger('backend_manufacturer')
		data = request.body
		data = json.loads(data.decode('utf8'))
		frontend_key = data["frontend_key"]
		manufacturer_id = data["manufacturer_id"]
		post_data = {"session_key": session_key}
		headers = {'Content-type': 'application/json'}	
		check = requests.post("http://localhost:8000/session/check/", data=json.dumps(post_data), headers=headers)
		if check.status_code == requests.codes.ok:
			try:
				manufacturer = Manufacturer.objects.get(pk=manufacturer_id)
				manufacturer.delete()
				data = json.dumps({"info":"Success deleting"})
				logger.info(data)
				return HttpResponse(data)
			except ObjectDoesNotExist:
				with open(os.path.join(settings.BASE_DIR, "static/jsons/manufacturer_not_found.json")) as data_file:    
					data = json.load(data_file)
				logger.info(data)
				return HttpResponse(json.dumps(data), status=404)
		else:
			with open(os.path.join(settings.BASE_DIR, "static/jsons/error_check.json")) as data_file:    
				data = json.load(data_file)
			logger.info(data)
			return HttpResponse(json.dumps(data), status=401)
		
	return HttpResponse("Ok")

@csrf_exempt
def add(request):
	if request.method == "POST":
		logger = logging.getLogger('backend_manufacturer')
		data = request.body
		data = json.loads(data.decode('utf8'))
		session_key = data["session_key"]
		name = data["name"]
		established = data["established"]
		country = data["country"]
		post_data = {"session_key": session_key}
		headers = {'Content-type': 'application/json'}	
		check = requests.post("http://localhost:8000/session/check/", data=json.dumps(post_data), headers=headers)
		if check.status_code == requests.codes.ok:
			try:
				manufacturer = Manufacturer.objects.create(name=name,established=established,country=country)
				manufacturer.save()
				data = json.dumps({"info":"Success adding"})
				logger.info(data)
				return HttpResponse(data)
			except ObjectDoesNotExist:
				with open(os.path.join(settings.BASE_DIR, "static/jsons/manufacturer_not_found.json")) as data_file:    
					data = json.load(data_file)
				logger.info(data)
				return HttpResponse(json.dumps(data), status=404)
		else:
			with open(os.path.join(settings.BASE_DIR, "static/jsons/error_check.json")) as data_file:    
				data = json.load(data_file)
			logger.info(data)
			return HttpResponse(json.dumps(data), status=401)
		
	return HttpResponse("Ok")