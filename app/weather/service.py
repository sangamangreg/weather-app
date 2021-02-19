from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from abc import ABC, abstractmethod
from urllib.parse import urlencode
from django.conf import settings
import requests
import json
from http import HTTPStatus
import logging
import requests_cache

requests_cache.install_cache('open_api_cache', expire_after=60 * settings.CACHE_DURATION_IN_MINUTES)


logger = logging.getLogger( __name__ )

directions = [_('North'), _('East'), _('South'), _('West')]


class Weather( object ):
    def __init__(self, name, temperature, min_temp, max_temp, humidity, pressure, wind_speed, direction, description):
        self.name = name
        self.temperature = temperature
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.humidity = humidity
        self.pressure = pressure
        self.wind_speed = wind_speed
        self.description = description
        ix = round( direction / (360. / 4) )
        self.direction = directions[ix % 4]

    def __str__(self):
        return "The city name is " + str(self.name) + " and temperature is " + str(self.temperature)


class WeatherService( ABC ):
    def __init__(self, url, **params):
        if self.__class__ == WeatherService:
            raise Exception( 'Can not instantiate Abstract class' )
        self.api_url = url + '?' + urlencode( params )

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def decoder_hook(self, data):
        pass


class OpenWeatherService( WeatherService ): # retry mechanism
    def get_data(self):
        logger.info( "Information to fetch weather infomration for city" )
        try:
            response = requests.get( self.api_url, timeout=3 )
            logger.info( "Information collected successfully" )
            if response.status_code == HTTPStatus.OK:
                weather_object = self.decoder_hook( json.loads( response.content ) )
                return weather_object
            else:
                response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.warning( "HTTP error while fetching data " + str(e) )
            raise
        except requests.exceptions.ConnectionError as e:
            logger.warning( "Error Connecting to openwaather " + str(e) )
            raise
        except requests.exceptions.Timeout as e:
            logger.warning( "Timeout Error. Openweather did not respond well in time" + str(e) )
            raise
        except requests.exceptions.RequestException as e:
            logger.warning( "Something went wrong while fetching information from openweatherapi " + str(e) )
            raise

    def decoder_hook(self, data):
        return Weather(
            name=data['name'],
            temperature=data['main']['temp'],
            min_temp=data['main']['temp_min'],
            max_temp=data['main']['temp_max'],
            humidity=data['main']['humidity'],
            pressure=data['main']['pressure'],
            wind_speed=data['wind']['speed'],
            direction=data['wind']['deg'],
            description=data['weather'][0]['description']
        )
