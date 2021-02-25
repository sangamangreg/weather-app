# Weather App

[![Working Demo](https://img.youtube.com/vi/KsXh8hzP1ik/0.jpg)](https://www.youtube.com/watch?v=KsXh8hzP1ik "CTRL+click to open in new tab")

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
  - `docker-compose build`
  - `docker-compose up`
  
#### Note:
    WEATHER_KEY can be obtained by signing up here `https://openweathermap.org/`

## Available URL's to navigate
- Home, [http:127.0.0.1:8000](http:127.0.0.1:8000)
- Climate, [http:127.0.0.1:8000/climate](http:127.0.0.1:8000/climate)


<img src="/app/static/images/English-Mumbai.png">
<img src="/app/static/images/German-Berlin.png">
<img src="/app/static/images/Spanish-Berlin.png"> 
