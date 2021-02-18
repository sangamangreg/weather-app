from __future__ import unicode_literals
from abc import ABC, abstractmethod
from urllib.parse import urlencode, quote_plus
import requests
import json
from http import HTTPStatus


directions = ['North', 'East', 'South', 'West']
class Weather(object):
    def __init__(self, name, temperature, min_temp, map_temp, humidity, pressure, wind_speed, direction, description):
        self.name = name
        self.temperature = temperature
        self.min_temp = min_temp
        self.map_temp = map_temp
        self.humidity = humidity
        self.pressure = pressure
        self.wind_speed = wind_speed
        self.direction = direction
        self.description = description
        ix = round( direction / (360. / 4) )
        self.direction = directions[ix % 4]


class WeatherService(ABC):
    def __init__(self, url, **params):
        if self.__class__ == WeatherService:
            raise Exception( 'Can not instantiate Abstract class' )

        self.url = url
        self.params = params

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def decoder_hook(self, data):
        pass

class OpenWeatherService(WeatherService):
    def get_data(self):
        API_URL = self.url + '?' + urlencode(self.params)
        print (API_URL)
        try:
            response = requests.get(API_URL)
            if response.status_code == HTTPStatus.OK:
                weather_object = self.decoder_hook( json.loads(response.content) )
                return weather_object
            else:
                raise Exception("TODO:: Exception Handling")
        except:
            raise RuntimeError("TODO:: Exception Handling")

    def decoder_hook(self, data):
        return Weather(
            name=data['name'],
            temperature=data['main']['temp'],
            min_temp=data['main']['temp_min'],
            map_temp=data['main']['temp_max'],
            humidity=data['main']['humidity'],
            pressure=data['main']['pressure'],
            wind_speed=data['wind']['speed'],
            direction=data['wind']['speed'],
            description=data['weather'][0]['main']
        )