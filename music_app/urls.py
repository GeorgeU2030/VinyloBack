from django.urls import path, include
from music_app.views import song_view, artist_view
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'songs', song_view.SongView, 'songs')

urlpatterns = [
    path('api/', include(router.urls)),
    path('last_week/', song_view.last_week, name='last_week'),
    path('update_artist/', artist_view.update_artist, name='update_artist'),
    path('new_current_date/', artist_view.update_current_date, name='new_current_date'),
    path('get_artist_month/', artist_view.get_artists_of_month, name='get_artist_month'),
]