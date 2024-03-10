from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.views import View
from background_task import background
from .forms import RegistrationForm
import os
import requests
import asyncio
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from dotenv import load_dotenv
from .utils import fetch_data_and_generate_pie_chart, get_registration_dates_from_database
from datetime import datetime
from django.db import connection

API_SERVER = os.getenv("API_SERVER")
headers = {
    "accept": "application/json"
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
                "email": email,
                "password": password,
                "username": username,
                "age": age
            }
            response = requests.post(API_SERVER + '/registration', headers=headers, json=data)
            print(f"{response.text}")
            response_data = response.json()
            print(f"reponse data kdsklsf{response_data}")
            request.session['registration_data'] = response_data["token"]
            registration_data = request.session.get('registration_data')
            return render(request, 'registration.html', {'token': response_data})

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def pie_chart_view(request):
    load_dotenv()
    api_url = "http://127.0.0.1:8000/dubbings-languages/"
    token = request.session.get('registration_data')

    # Create an event loop and run the asynchronous function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    chart_base64 = loop.run_until_complete(fetch_data_and_generate_pie_chart(api_url, token))

    # Pass data to the template
    context = {"chart_base64": chart_base64}

    # Render the template with the pie chart
    return render(request, "stats.html", context)

async def generate_column_chart(request):
    # Execute your stored procedure or retrieve registration dates from the database
    # Replace this with your actual database query
    api_url = "http://127.0.0.1:8000/registration-info"
    token = request.session.get('registration_data')

    registration_dates = await get_registration_dates_from_database(api_url, token)

    # Process registration dates
    date_counts = {}
    for date_str in registration_dates:
        try:
            date = datetime.strptime(date_str['registration_date'], "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            # If microseconds are not present, use a different format
            date = datetime.strptime(date_str['registration_date'], "%Y-%m-%d %H:%M:%S")

        # Extract only date portion without microseconds
        formatted_date = date.strftime("%Y-%m-%d")

        date_counts[formatted_date] = date_counts.get(formatted_date, 0) + 1

    # Sort dates for ordered plotting
    sorted_dates = sorted(date_counts.keys())

    plt.figure(figsize=(26, 8))

    # Generate column chart
    plt.bar(sorted_dates, [date_counts[date] for date in sorted_dates])
    plt.xlabel('Registration Dates')
    plt.ylabel('Number of Users')
    plt.title('User Registrations Over Time')

    # Save the chart to BytesIO and encode to base64
    chart_image = BytesIO()
    plt.savefig(chart_image, format="png")
    chart_image.seek(0)
    plt.close()

    chart_base64 = base64.b64encode(chart_image.read()).decode("utf-8")

    # Pass the chart data to the template
    return render(request, 'registration_info.html', {'chart_base64': chart_base64})


