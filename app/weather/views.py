from __future__ import unicode_literals

from django.utils.translation import get_language_from_request
from django.shortcuts import render
from weather.service import OpenWeatherService
from django.conf import settings
from weather.forms import CityForm
import requests


def index(request):
    weather_object = None
    if request.method == 'POST':
        form = CityForm( request.POST )
        if form.is_valid():
            language = get_language_from_request(request)
            weather_service = OpenWeatherService(settings.CHEMONDIS_OPENWEATHER_URL, q=form.cleaned_data['city'], appid=settings.CHEMONDIS_WEATHER_KEY, units="metric", lang=language)
            try:
                weather_object = weather_service.get_data()
                print(str(weather_object))
            except requests.exceptions.HTTPError as e:
                form.add_error('city', 'Please enter valid city name')
            except requests.exceptions.ConnectionError as e:
                form.add_error( 'city', 'System id down. Try in some time' )
            except requests.exceptions.Timeout as e:
                form.add_error( 'city', 'Server taking too much time to respond. Try in some time' )
            except requests.exceptions.RequestException as e:
                form.add_error( 'city', 'Please enter valid city name' )
    else:
        form = CityForm()

    args = {
        "weather_object": weather_object,
        "form": form
    }
    return render(request, 'weather/index.html', args)