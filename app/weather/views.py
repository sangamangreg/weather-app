from __future__ import unicode_literals

from django.views.decorators.cache import cache_page
from django.utils.translation import get_language_from_request
from django.shortcuts import render, redirect
from weather.service import OpenWeatherService
from django.contrib import messages
from django.conf import settings
from weather.forms import CityForm
import requests
import logging
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger( __name__ )

def index(request):
    weather_object = None
    if request.method == 'POST':
        form = CityForm( request.POST )
        if form.is_valid():
            logger.info( "process started to fetch data" )
            language = get_language_from_request(request)
            weather_service = OpenWeatherService(settings.CHEMONDIS_OPENWEATHER_URL, q=form.cleaned_data['city'], appid=settings.CHEMONDIS_WEATHER_KEY, units="metric", lang=language)
            try:
                weather_object = weather_service.get_data()
                logger.info( "weather information found" )
            except requests.exceptions.HTTPError as e:
                form.add_error('city', _('Please enter valid city name'))
            except requests.exceptions.ConnectionError as e:
                form.add_error( 'city', _('System id down. Try in some time' ))
            except requests.exceptions.Timeout as e:
                form.add_error( 'city', _('Server taking too much time to respond. Try in some time' ))
            except requests.exceptions.RequestException as e:
                form.add_error( 'city', _('Please enter valid city name' ))
    else:
        form = CityForm()

    args = {
        "weather_object": weather_object,
        "form": form
    }
    return render(request, 'weather/index.html', args)


def climate(request):
    if request.method == 'POST':
        form = CityForm( request.POST )
        if form.is_valid():
            return redirect(climate_for_city, form.cleaned_data['city'])
    else:
        form = CityForm()

    args = {
        "form": form
    }
    return render( request, 'weather/climate.html', args )


@cache_page(60 * settings.CACHE_DURATION_IN_MINUTES)
def climate_for_city(request, city):
    weather_object = None
    language = get_language_from_request( request )
    weather_service = OpenWeatherService( settings.CHEMONDIS_OPENWEATHER_URL, q=city,
                                          appid=settings.CHEMONDIS_WEATHER_KEY, units="metric", lang=language )
    try:
        weather_object = weather_service.get_data()
    except requests.exceptions.HTTPError as e:
        messages.error( request, _('Please enter valid city name') )
        return redirect(climate)
    except requests.exceptions.ConnectionError as e:
        messages.error( request, _('System id down. Try in some time' ))
        return redirect( climate )
    except requests.exceptions.Timeout as e:
        messages.error( request, _('Server taking too much time to respond. Try in some time' ))
        return redirect( climate )
    except requests.exceptions.RequestException as e:
        messages.error( request, _('Please enter valid city name' ))
        return redirect( climate )

    args = {
        "weather_object": weather_object
    }
    return render( request, 'weather/climate-city.html', args )