from django.urls import path
from . import views


urlpatterns = [
    path(r'', views.index ),
    path('climate', views.climate, name='climate'),
    path('climate/<str:city>', views.climate_for_city, name='city_climate')
]
