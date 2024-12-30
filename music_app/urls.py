from django.urls import path
from music_app.views import song_view

urlpatterns = [
    path('last_week/', song_view.last_week, name='last_week'),
]