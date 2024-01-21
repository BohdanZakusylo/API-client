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

def set_token_in_session(request, token):
    request.session['my_token'] = token
    return HttpResponse("Token set in session.")

'''
async def get(url, headers=headers, params={}):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response
    except httpx.HTTPError as e:
        print(e)

async def post(api_server, end_point, headers=headers, data={}):
    url = api_server + end_point
    try:
        with httpx.AsyncClient as client:
            response: httpx.Response = await client.post(url, headers=headers, data=data)
            response.raise_for_status()
            return response
    except httpx.HTTPError as e:
        print(e)
'''

def index(request):
    return render(request, "home.html")


def test_backend(request):
    print(request.session.get('registration_data'))
    API_SERVER = os.getenv("API_SERVER")
    if not API_SERVER:
        raise EnvironmentError("no API_SERVER defined")
    try:
        data = requests.get(f"{API_SERVER}/")
    except requests.HTTPError as e:
        data = {'error': str(e)}
    return render(request, "test_backend.html", {"data": "Cleint is connected to the backend"})


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
                "password": password,
                "email": email,
                "age": age
            }
            response = requests.post(API_SERVER + '/registration', headers=headers, json=data)
            response_data = response.json()
            request.session['registration_data'] = response_data
            registration_data = request.session.get('registration_data')
            return render(request, 'registration.html', {'token': response_data})

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

