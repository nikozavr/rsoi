from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import requests
import json
from django.core.cache import cache
from django.contrib import messages
from requests.exceptions import ConnectionError

# Create your views here.
def home(request):
    return HttpResponse("OK")

@csrf_exempt
def index(request):
#    post_data = {"login":"nikozavr",
#                "password":"nikitos1"}

#    headers = {'Content-type': 'application/json'}
    if 'session_key' in request.session:
        post_data = {"session_key":request.session['session_key']}
        headers = {'Content-type': 'application/json'}
        r_user_session = requests.post("http://session.mobileparts.ru/check/", data=json.dumps(post_data), headers=headers) 
        if r_user_session.status_code == requests.codes.ok:
            data_session_user = r_user_session.json()
            user_id = data_session_user["id"]
            try:
                r_user = requests.get("http://users.mobileparts.ru/info/" + str(user_id))
                if r_user.status_code == requests.codes.ok:
                    data_user = r_user.json()
                    print(data_user)
                    context = {
                                 "data_user": data_user
                              }
                    return render(request, 'interface/index.html', context)
                else:
                    del request.session['session_key']
                    context = {
                                 "data_user": 0,
                                 "error_text": "User information is not available"
                              }
                    return render(request, 'interface/index.html', context)
            except ConnectionError:
                del request.session['session_key']
                context = {
                             "data_user": 0,
                             "error_text": "User information is not available"
                          }
                return render(request, 'interface/index.html', context)
        else:
            context = {
                             "data_user": 0
                          }
            return render(request, 'interface/index.html', context)
    else:
        context = {
                         "data_user": 0
                      }
        return render(request, 'interface/index.html', context)

    return HttpResponse("Ok")
    
    
"""
    r_manufacturers = requests.get("http://localhost:8000/backend_manufacturers/list/")
    try:
        data_manufacturers = r_manufacturers.json()
    except ValueError:
        data_manufacturers = {"count": 0}

    r_devices = requests.get("http://localhost:8000/backend_devices/list/")    
    
    try:
        data_devices = r_devices.json()    
    except ValueError:
        data_devices = {"count": 0}
    if 'session_key' in request.session:
        post_data = {"session_key":request.session['session_key']}
        headers = {'Content-type': 'application/json'}
        logger.info(post_data)
        r_user = requests.post("http://localhost:8000/session/userinfo/", data=json.dumps(post_data), headers=headers) 
        if r_user.status_code == requests.codes.ok:
            data_user = r_user.json()
            context = { "data_manufacturers": data_manufacturers,
                        "data_devices": data_devices,
                        "data_user": data_user                                
                        }
        else:
            context = { "data_manufacturers": data_manufacturers,
                        "data_devices": data_devices,
                        "data_user": 0                            
                        }
        return render(request, 'frontend/index.html', context)
    

    else:
        context = { "data_manufacturers": data_manufacturers,
                        "data_devices": data_devices,
                        "data_user": 0                            
                        }"""

#    context = { "data_manufacturers": "s",
#                        "data_devices": "data_devices",
#                        "data_user": 0                            
#                        }

"""
def check_user(request):
    post_data = {""}
    return HttpResponse("Ok")

def requests_manager(request):
    return HttpResponse("OK")
"""
def register(request):
    return HttpResponse("OK")


@csrf_exempt
def login(request):
    if request.method == "POST":
        error_text = ""
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        post_data = {"username":username,
                "password":password}

        headers = {'Content-type': 'application/json'}  

        r = requests.post("http://session.mobileparts.ru/create/session/", data=json.dumps(post_data), headers=headers) 

        if r.status_code == requests.codes.ok:
            data = r.json()
            request.session['session_key'] = data["session_key"]
            return redirect("http://mobileparts.ru:8000/")
        else:
            error_text = "Password is incorrect"
            return render(request, 'interface/authorize.html', {"error_text": error_text})

    if request.method == "GET":
        return render(request, 'interface/authorize.html', )    
    return HttpResponse("Ok")

def logout(request):
    try:
        s = request.session['session_key']
        headers = {'Content-type': 'application/json'}
        post_data = {"session_key":s}
        r = requests.post("http://session.mobileparts.ru/session/close/", data=json.dumps(post_data), headers=headers) 
        if r.status_code == requests.codes.ok:
            del request.session['session_key']
            return redirect("http://mobileparts.ru:8000/")
    except KeyError:
        pass
    return redirect("http://mobileparts.ru:8000/")

def manufacturers(request):
    r_manufacturers = requests.get("http://manufacturers.mobileparts.ru/list/")
    try:
        data_manufacturers = r_manufacturers.json()
    except ValueError:
        data_manufacturers = {"count": 0}

    if 'session_key' in request.session:
        post_data = {"session_key":request.session['session_key']}
        headers = {'Content-type': 'application/json'}
        r_user_session = requests.post("http://session.mobileparts.ru/check/", data=json.dumps(post_data), headers=headers) 
        if r_user_session.status_code == requests.codes.ok:
            data_session_user = r_user_session.json()
            user_id = data_session_user["id"]
            try:
                r_user = requests.get("http://users.mobileparts.ru/info/" + str(user_id))
                if r_user.status_code == requests.codes.ok:
                    data_user = r_user.json()
                    print(data_user)
                    context = {
                                 "data_user": data_user,
                                 "data_manufacturers":data_manufacturers
                              }
                    return render(request, 'interface/manufacturers.html', context)
                else:
                    del request.session['session_key']
                    context = {
                                 "data_user": 0,
                                 "error_text": "User information is not available",
                                 "data_manufacturers":data_manufacturers
                              }
                    return render(request, 'interface/manufacturers.html', context)
            except ConnectionError:
                del request.session['session_key']
                context = {
                             "data_user": 0,
                             "error_text": "User information is not available",
                                 "data_manufacturers":data_manufacturers
                          }
                return render(request, 'interface/manufacturers.html', context)
        else:
            context = {
                             "data_user": 0,
                                 "data_manufacturers":data_manufacturers
                          }
            return render(request, 'interface/manufacturers.html', context)
    else:
        context = {
                         "data_user": 0,
                                 "data_manufacturers":data_manufacturers
                      }
        return render(request, 'interface/manufacturers.html', context)

    return HttpResponse("Ok")

def devices(request):
    r_manufacturers = requests.get("http://manufacturers.mobileparts.ru/list/")
    try:
        data_manufacturers = r_manufacturers.json()
    except ValueError:
        data_manufacturers = {"count": 0}

    r_devices = requests.get("http://devices.mobileparts.ru/list/")
    try:
        data_devices = r_devices.json()
        for device in data_devices["devices"]:
            for manufacturer in data_manufacturers["manufacturers"]:
                if manufacturer["id"] == device["manufacturer_id"]:
                    device["manufacturer_id"] = manufacturer["name"]
    except ValueError:
        data_devices = {"count": 0}


    if 'session_key' in request.session:
        post_data = {"session_key":request.session['session_key']}
        headers = {'Content-type': 'application/json'}
        r_user_session = requests.post("http://session.mobileparts.ru/check/", data=json.dumps(post_data), headers=headers) 
        if r_user_session.status_code == requests.codes.ok:
            data_session_user = r_user_session.json()
            user_id = data_session_user["id"]
            try:
                r_user = requests.get("http://users.mobileparts.ru/info/" + str(user_id))
                if r_user.status_code == requests.codes.ok:
                    data_user = r_user.json()
                    print(data_user)
                    context = {
                                 "data_user": data_user,
                                 "data_devices":data_devices
                              }
                    return render(request, 'interface/devices.html', context)
                else:
                    del request.session['session_key']
                    context = {
                                 "data_user": 0,
                                 "error_text": "User information is not available",
                                 "data_devices":data_devices
                              }
                    return render(request, 'interface/devices.html', context)
            except ConnectionError:
                del request.session['session_key']
                context = {
                             "data_user": 0,
                             "error_text": "User information is not available",
                                 "data_devices":data_devices
                          }
                return render(request, 'interface/devices.html', context)
        else:
            context = {
                             "data_user": 0,
                                 "data_devices":data_devices
                          }
            return render(request, 'interface/devices.html', context)
    else:
        context = {
                         "data_user": 0,
                                 "data_devices":data_devices
                      }
        return render(request, 'interface/devices.html', context)
    return HttpResponse("Ok")

def parts(request):
    r_devices = requests.get("http://devices.mobileparts.ru/list/")
    try:
        data_devices = r_devices.json()
    except ValueError:
        data_devices = {"count": 0}

    r_parts = requests.get("http://parts1.mobileparts.ru/list/")
    try:
        data_parts = r_parts.json()
        for part in data_parts["parts"]:
            for device in data_devices["devices"]:
                if device["id"] == part["device_id"]:
                    part["device_id"] = device["model_name"]
    except ValueError:
        data_parts = {"count": 0}


    if 'session_key' in request.session:
        post_data = {"session_key":request.session['session_key']}
        headers = {'Content-type': 'application/json'}
        r_user_session = requests.post("http://session.mobileparts.ru/check/", data=json.dumps(post_data), headers=headers) 
        if r_user_session.status_code == requests.codes.ok:
            data_session_user = r_user_session.json()
            user_id = data_session_user["id"]
            try:
                r_user = requests.get("http://users.mobileparts.ru/info/" + str(user_id))
                if r_user.status_code == requests.codes.ok:
                    data_user = r_user.json()
                    print(data_user)
                    context = {
                                 "data_user": data_user,
                                 "data_parts":data_parts
                              }
                    return render(request, 'interface/parts.html', context)
                else:
                    del request.session['session_key']
                    context = {
                                 "data_user": 0,
                                 "error_text": "User information is not available",
                                 "data_parts":data_parts
                              }
                    return render(request, 'interface/parts.html', context)
            except ConnectionError:
                del request.session['session_key']
                context = {
                             "data_user": 0,
                             "error_text": "User information is not available",
                                  "data_parts":data_parts
                          }
                return render(request, 'interface/parts.html', context)
        else:
            context = {
                             "data_user": 0,
                                 "data_parts":data_parts
                          }
            return render(request, 'interface/parts.html', context)
    else:
        context = {
                         "data_user": 0,
                                 "data_parts":data_parts
                      }
        return render(request, 'interface/parts.html', context)
    return HttpResponse("Ok")

def info_part(request, part_id):
    r_devices = requests.get("http://devices.mobileparts.ru/list/")
    try:
        data_devices = r_devices.json()
    except ValueError:
        data_devices = {"count": 0}

    r_part = requests.get("http://parts1.mobileparts.ru/info/"+str(part_id))
    try:
        part = r_part.json() 
        
    except ValueError:
        part = {"id": 0}


    r_rev = requests.get("http://review1.mobileparts.ru/list/device/"+str(part["device_id"]))
    try:
        data_reviews = r_rev.json()
    except ValueError:
        data_reviews = {"count": 0}    

    for device in data_devices["devices"]:
        if device["id"] == part["device_id"]:
            part["device_id"] = device["model_name"]
    

    if 'session_key' in request.session:
        post_data = {"session_key":request.session['session_key']}
        headers = {'Content-type': 'application/json'}
        r_user_session = requests.post("http://session.mobileparts.ru/check/", data=json.dumps(post_data), headers=headers) 
        if r_user_session.status_code == requests.codes.ok:
            data_session_user = r_user_session.json()
            user_id = data_session_user["id"]
            try:
                r_user = requests.get("http://users.mobileparts.ru/info/" + str(user_id))
                if r_user.status_code == requests.codes.ok:
                    data_user = r_user.json()
                    print(data_user)
                    context = {
                                 "data_user": data_user,
                                 "part":part,
                                 "data_reviews": data_reviews
                              }
                    return render(request, 'interface/info_part.html', context)
                else:
                    del request.session['session_key']
                    context = {
                                 "data_user": 0,
                                 "error_text": "User information is not available",
                                 "part":part,
                                 "data_reviews":data_reviews
                              }
                    return render(request, 'interface/info_part.html', context)
            except ConnectionError:
                del request.session['session_key']
                context = {
                             "data_user": 0,
                             "error_text": "User information is not available",
                                  "part":part,
                                  "data_reviews": data_reviews
                          }
                return render(request, 'interface/info_part.html', context)
        else:
            context = {
                             "data_user": 0,
                                 "part":part,
                              "data_reviews": data_reviews
                          }
            return render(request, 'interface/info_part.html', context)
    else:
        context = {
                         "data_user": 0,
                                 "part":part,
                                 "data_reviews": data_reviews
                      }
        return render(request, 'interface/info_part.html', context)
    return HttpResponse("Ok")

"""
def del_device(request, device_id):
    if request.method == "GET":
        logger = logging.getLogger('lab3')
        if 'session_key' in request.session:
            post_data = {"session_key":request.session['session_key'], "device_id": device_id}
            headers = {'Content-type': 'application/json'}
            logger.info(post_data)
            result = requests.post("http://localhost:8000/backend_devices/remove/", data=json.dumps(post_data), headers=headers) 
            if result.status_code == requests.codes.ok:
                return redirect("http://localhost:8000/")
            else:
                messages.add_message(request, messages.INFO, 'Hello world.')


    return HttpResponse("Ok")


def del_manufacturer(request, manufacturer_id):
    if request.method == "GET":
        logger = logging.getLogger('lab3')
        if 'session_key' in request.session:
            post_data = {"session_key":request.session['session_key'], "manufacturer_id": manufacturer_id}
            headers = {'Content-type': 'application/json'}
            logger.info(post_data)
            result = requests.post("http://localhost:8000/backend_manufacturers/remove/", data=json.dumps(post_data), headers=headers) 
            if result.status_code == requests.codes.ok:
                return redirect("http://localhost:8000/")
            else:
                messages.add_message(request, messages.ERROR, 'Error delete')

    return HttpResponse("Ok")


def edit_device(request, device_id):
    if request.method == "GET":
        if 'session_key' in request.session:
            logger = logging.getLogger('lab3')
            post_data = {"session_key":request.session['session_key']}
            headers = {'Content-type': 'application/json'}
            logger.info(post_data)
            r_user = requests.post("http://localhost:8000/session/userinfo/", data=json.dumps(post_data), headers=headers) 
            r_device = requests.get("http://localhost:8000/backend_devices/list/"+device_id+"/")
            try:
                data_device = r_device.json()
            except ValueError:
                data_device = {"count": 0}
            r_manufacturers = requests.get("http://localhost:8000/backend_manufacturers/list/")
            try:
                data_manufacturers = r_manufacturers.json()
            except ValueError:
                data_manufacturers = {"count": 0}
            
            if r_user.status_code == requests.codes.ok:
                data_user = r_user.json()
                context = {"data_user": data_user,
                            "data_manufacturers": data_manufacturers,
                            "data_device": data_device["device"]

                            }
            else:
                context = {    "data_user": 0,
                            "data_manufacturers": data_manufacturers,
                            "data_device": data_device["device"]
                            }
            return render(request, "frontend/edit_device.html", context)
    if request.method == "POST":
        if 'session_key' in request.session:
            logger = logging.getLogger('lab3')
            name = request.POST.get("name","")
            manufacturer_id = request.POST.get("manufacturer_id","")
            device_type = request.POST.get("device_type","")
            dig_disp = request.POST.get("dig_disp","")
            year = request.POST.get("year","")
            post_data = {"session_key":request.session['session_key'], "name": name, "manufacturer_id":manufacturer_id, "device_type": device_type, "dig_disp":dig_disp, "year": year}
            headers = {'Content-type': 'application/json'}
            logger.info(post_data)
            result = requests.post("http://localhost:8000/backend_devices/add/", data=json.dumps(post_data), headers=headers) 
            if result.status_code == requests.codes.ok:
                return redirect("http://localhost:8000/")
            else:
                messages.add_message(request, messages.INFO, 'Error add.')



def edit_manufacturer(request, manufacturer_id):

    return HttpResponse("Ok")

def add_device(request):
    if request.method == "GET":
        if 'session_key' in request.session:
            logger = logging.getLogger('lab3')
            post_data = {"session_key":request.session['session_key']}
            headers = {'Content-type': 'application/json'}
            logger.info(post_data)
            r_user = requests.post("http://localhost:8000/session/userinfo/", data=json.dumps(post_data), headers=headers) 
            r_manufacturers = requests.get("http://localhost:8000/backend_manufacturers/list/")
            try:
                data_manufacturers = r_manufacturers.json()
            except ValueError:
                data_manufacturers = {"count": 0}
            if r_user.status_code == requests.codes.ok:
                data_user = r_user.json()
                context = {"data_user": data_user,
                            "data_manufacturers": data_manufacturers
                            }
            else:
                context = {    "data_user": 0,
                            "data_manufacturers": data_manufacturers
                            }
            return render(request, "frontend/add_device.html", context)
    if request.method == "POST":
        if 'session_key' in request.session:
            logger = logging.getLogger('lab3')
            name = request.POST.get("name","")
            manufacturer_id = request.POST.get("manufacturer_id","")
            device_type = request.POST.get("device_type","")
            dig_disp = request.POST.get("dig_disp","")
            year = request.POST.get("year","")
            post_data = {"session_key":request.session['session_key'], "name": name, "manufacturer_id":manufacturer_id, "device_type": device_type, "dig_disp":dig_disp, "year": year}
            headers = {'Content-type': 'application/json'}
            logger.info(post_data)
            result = requests.post("http://localhost:8000/backend_devices/add/", data=json.dumps(post_data), headers=headers) 
            if result.status_code == requests.codes.ok:
                return redirect("http://localhost:8000/")
            else:
                messages.add_message(request, messages.INFO, 'Error add.')


def add_manufacturer(request):
    if request.method == "GET":
        if 'session_key' in request.session:
            logger = logging.getLogger('lab3')
            post_data = {"session_key":request.session['session_key']}
            headers = {'Content-type': 'application/json'}
            logger.info(post_data)
            r_user = requests.post("http://localhost:8000/session/userinfo/", data=json.dumps(post_data), headers=headers) 
            if r_user.status_code == requests.codes.ok:
                data_user = r_user.json()
                context = {"data_user": data_user                                
                            }
            else:
                context = {    "data_user": 0                            
                            }
            return render(request, "frontend/add_manufacturer.html", context)
    if request.method == "POST":
        if 'session_key' in request.session:
            logger = logging.getLogger('lab3')
            name = request.POST.get("name","")
            established = request.POST.get("established","")
            country = request.POST.get("country","")
            post_data = {"session_key":request.session['session_key'], "name": name, "established":established, "country": country}
            headers = {'Content-type': 'application/json'}
            logger.info(post_data)
            result = requests.post("http://localhost:8000/backend_manufacturers/add/", data=json.dumps(post_data), headers=headers) 
            if result.status_code == requests.codes.ok:
                return redirect("http://localhost:8000/")
            else:
                messages.add_message(request, messages.INFO, 'Error add.')


"""