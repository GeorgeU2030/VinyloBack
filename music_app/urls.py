from django.urls import path, include
from music_app.views import song_view
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'songs', song_view.SongView, 'songs')

urlpatterns = [
    path('api/', include(router.urls)),
    path('last_week/', song_view.last_week, name='last_week'),
]