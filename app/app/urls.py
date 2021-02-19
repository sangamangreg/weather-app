from django.urls import path, include


urlpatterns = [
    path(r'', include('weather.urls')),
]
