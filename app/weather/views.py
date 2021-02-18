from __future__ import unicode_literals

from django.shortcuts import render
from weather.service import OpenWeatherService
from django.conf import settings
import requests
import json



def index(request):
    weather_service = OpenWeatherService(settings.CHEMONDIS_OPENWEATHER_URL, id='1275339', appid=settings.CHEMONDIS_OPENWEATHER_KEY)
    weather_object = weather_service.get_data()
    print (weather_object.direction)
    return render(request, 'weather/index.html')
