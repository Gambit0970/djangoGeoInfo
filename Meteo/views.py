from datetime import datetime, timedelta
import geocoder as geocoder
import timezonefinder, pytz
from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.template import loader

from Meteo.models import Worldcities


def get_timezone(location):
    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lat=location[0], lng=location[1])
    dt = datetime.utcnow()
    if timezone_str:
        # Display the current time in that time zone
        timezone = pytz.timezone(timezone_str)
        return timezone_str, dt + timezone.utcoffset(dt)


def get_temp(location):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    api_request = f"{endpoint}?latitude={location[0]}&longitude={location[1]}&hourly=temperature_2m"
    meteo_data = requests.get(api_request).json()
    now = datetime.now()
    hour = now.hour
    temp = meteo_data['hourly']['temperature_2m'][hour]
    return temp


def temp_here(request):
    location = geocoder.ip('me').latlng
    temp = get_temp(location)
    tzS, tzD = get_timezone(location)
    template = loader.get_template('index.html')
    context = {'city': 'Your Location',
               'zone': tzS,
               'date': tzD.date(),
               'time': tzD.time(),
               'temp': temp,
               'lat': location[0],
               'long': location[1]}
    return HttpResponse(template.render(context, request))


def temp_somewhere(request):
    random_item = Worldcities.objects.all().order_by('?').first()
    city = random_item.city
    location = [random_item.lat, random_item.lng]
    temp = get_temp(location)
    tzS, tzD = get_timezone(location)
    template = loader.get_template("index.html")
    context = {'city': city,
               'zone': tzS.replace("_"," "),
               'date': tzD.date(),
               'time': tzD.time(),
               'temp': temp,
               'lat': location[0],
               'long': location[1]}
    return HttpResponse(template.render(context, request))
