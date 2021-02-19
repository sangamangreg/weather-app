from django.urls import path, include


urlpatterns = [
    path(r'', include('weather.urls')),
]

handler404 = 'weather.views.error_404'
handler500 = 'weather.views.error_500'
handler403 = 'weather.views.error_403'
handler400 = 'weather.views.error_400'