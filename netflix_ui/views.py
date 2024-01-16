from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.views import View
from .forms import RegistrationForm
import os
import requests


API_SERVER = os.getenv("API_SERVER")
headers = {
    "Content-Type": "application/json"
}
if not API_SERVER:
    raise EnvironmentError("no API_SERVER defined in .env")

def get(endpoint, headers=headers, server=API_SERVER):
    return requests.get(server+endpoint, headers=headers)



def index(request):
    return HttpResponse("Hello world!")


def test_backend(request):
    API_SERVER = os.getenv("API_SERVER")
    if not API_SERVER:
        raise EnvironmentError("no API_SERVER defined")
    try:
        data = get("/").json()
    except requests.RequestException as e:
        data = {'error': str(e)}
       # return render(request, "error.html", {'error_code': 500, 'error_msg': 'Server error'})
    return render(request, "test_backend.html", {"data": data})


def error_view(request, error_code, error_msg):
    return render(request, "error.html", {'error_code': error_code, 'error_msg': error_msg})


def registration_view(request):
    API_SERVER = os.getenv("API_SERVER")
    if not API_SERVER:
        raise EnvironmentError("no API_SERVER defined")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            age = form.cleaned_data['age']
            headers={"Content-Type": "application/json"}
            data = {
                "username": username,
                "email": email,
                "password": password,
                "age": age,
            }
            print(data)
            response = requests.post(API_SERVER + '/registration', headers=headers, json=data)
            response_data = response.json()
            if not 'token' in headers.keys() and 'token' in response_data():
                headers.update({'token': response_data['token']})

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

