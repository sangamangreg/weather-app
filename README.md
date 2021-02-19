# Weather App

## Problem statement
Design an application where use is able to check weather condition for any given valid city. Application should have capability to support multiple languages.


## Application demonstrates to use
- Open Weather API `https://openweathermap.org/`
- Multilingual support (English, German, Spanish)

## Tech Stack
- Python - Django Framework
- Docker

## Installation Guide
- Create a .env file and add two lines in it
  -  SECRET_KEY={value}
  -  WEATHER_KEY={value}
- Run below command
  - `cd <project_root_directory>`
  - `docker-compose up`
  
#### Note:
    WEATHER_KEY can be obtained by signing up here `https://openweathermap.org/`

## Available URL's to navigate
- Home, [http:127.0.0.1:8000](http:127.0.0.1:8000)
- Climate, [http:127.0.0.1:8000/climate](http:127.0.0.1:8000/climate)


<img src="/app/static/images/English-Mumbai.png"> 