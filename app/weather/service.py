from __future__ import unicode_literals
from abc import ABC, abstractmethod
from urllib.parse import urlencode, quote_plus
import requests
import json
from http import HTTPStatus
import datetime
import logging


logger = logging.getLogger(__name__)


directions = ['North', 'East', 'South', 'West']
class Weather(object):
    def __init__(self, name, temperature, min_temp, max_temp, humidity, pressure, wind_speed, direction, description, timezone):
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
        self.time = datetime.datetime.fromtimestamp(timezone).strftime('%H:%I %p %d %b %Y')


class WeatherService(ABC):
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

class OpenWeatherService(WeatherService):
    def get_data(self):
        logger.info("information to fetch weather infomration for city")
        try:
            response = requests.get(self.api_url)
            logger.info( "Information collected successfully" )
            if response.status_code == HTTPStatus.OK:
                weather_object = self.decoder_hook( json.loads(response.content) )
                return weather_object
            else:
                logger.warn( "Couldn't fetch the information" )
                raise Exception("TODO:: Exception Handling")
        except:
            logger.warn( "Exception occurred while fetching data from openweather api" )
            raise RuntimeError("TODO:: Exception Handling")

    def decoder_hook(self, data):
        return Weather(
            name=data['name'],
            temperature=data['main']['temp'],
            min_temp=data['main']['temp_min'],
            max_temp=data['main']['temp_max'],
            humidity=data['main']['humidity'],
            pressure=data['main']['pressure'],
            wind_speed=data['wind']['speed'],
            direction=data['wind']['speed'],
            description=data['weather'][0]['main'],
            timezone=data['dt'] + data['timezone']
        )