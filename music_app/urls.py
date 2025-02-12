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
    path('add_month_award/', artist_view.add_month_award, name='add_month_award'),
    path('get_allsongs/', song_view.get_all_songs, name='get_allsongs'),
    path('ranking/', artist_view.ranking, name='ranking'),
    path('ranking_awards/', artist_view.ranking_awards, name='ranking_awards'),
    path('get_awards_history/', artist_view.get_awards_history, name='get_awards_history'),
    path('ranking_period/<str:period_rank>', artist_view.rankings_by_history, name='ranking_period'),
    path('stats/', artist_view.stats, name='stats'),
    path('get_artist/<int:artist_id>', artist_view.get_artist, name='get_artist'),
    path('get_song_artist/<int:artist_id>', song_view.get_songs_by_artist, name='get_song_artist'),
    path('award_artist/<int:artist_id>', artist_view.awards_artist, name='award_artist'),
]