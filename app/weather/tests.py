from __future__ import unicode_literals

from django.test import TestCase
from weather.service import OpenWeatherService
from django.conf import settings
from unittest.mock import patch
import requests


class WeatherTestCase(TestCase):

    def test_success_scenario(self):
        weather_service = OpenWeatherService( settings.OPENWEATHER_URL, q='mumbai',
                                              appid=settings.WEATHER_KEY, units="metric", lang='en' )
        weather_object = weather_service.get_data()
        self.assertEquals(weather_object.name.lower(), 'mumbai')


    def test_wrong_api_key(self):
        weather_service = OpenWeatherService( settings.OPENWEATHER_URL, q='mumbai',
                                              appid='asq3sadad', units="metric", lang='en' )
        self.assertRaises(requests.exceptions.HTTPError, weather_service.get_data)


    def test_invalid_city(self):
        weather_service = OpenWeatherService( settings.OPENWEATHER_URL, q='a',
                                              appid=settings.WEATHER_KEY, units="metric", lang='en' )
        self.assertRaises(requests.exceptions.HTTPError, weather_service.get_data)

    def test_empty_city(self):
        weather_service = OpenWeatherService( settings.OPENWEATHER_URL, q='',
                                              appid=settings.WEATHER_KEY, units="metric", lang='en' )
        self.assertRaises(requests.exceptions.HTTPError, weather_service.get_data)


    # def test_limit_reached(self):
    #     with patch("weather.service.requests.get") as mock:
    #         mock.return_value.status_code = 429
    #         weather_service = OpenWeatherService( settings.OPENWEATHER_URL, q='mumbai',
    #                                       appid=settings.WEATHER_KEY, units="metric", lang='en' )
    #
    #     self.assertRaises(requests.exceptions.RequestException, weather_service.get_data)