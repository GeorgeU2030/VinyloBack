from rest_framework import viewsets, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from music_app.models import Song, Artist, User
from music_app.serializers import SongSerializer
from datetime import datetime

# Create the song and add the artists
class SongView(viewsets.ModelViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()

    def create(self, request, *args, **kwargs):
        # Get the user for add the artists
        profile = request.data.get('profile')
        user = User.objects.get(id=profile)
        # Get the artists for add the song
        artists_data = request.data.get('artists')

        artists_ids = [] 
        # Verify if the artists exists in the user
        if not profile:
            return Response({'error': 'Profile is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            for artist in artists_data:
                if Artist.objects.filter(profile=request.user, name=artist['name']).exists():
                    artist = Artist.objects.get(profile=request.user, name=artist['name'])
                    artists_ids.append(artist.id)
                else:
                    artist_info = {
                        'name': artist['name'],
                        'photo': artist['photo'],
                        'flag': artist['flag'],
                        'country': artist['country'],
                        'followers': artist['followers'],
                        'genres': artist['genres'],
                        'profile': user
                    }
                
                    artist = Artist.objects.create(**artist_info)
                    artists_ids.append(artist.id)

        # Get the dates and format them
        date_str = request.data.get('start_date')
        date = datetime.strptime(date_str, "%Y-%m-%d")  

        date_str_2 = request.data.get('end_date')
        date_2 = datetime.strptime(date_str_2, "%Y-%m-%d")  

        release_date_str = request.data.get('release_date')
        date_3 = datetime.strptime(release_date_str, "%Y-%m-%d")  

        start_formatted_date = date.strftime("%Y-%m-%d")
        end_formatted_date = date_2.strftime("%Y-%m-%d")
        release_formatted_date = date_3.strftime("%Y-%m-%d")

        # Add the song
        song_info = {
            'name': request.data.get('name'),
            'rating': request.data.get('rating'),
            'start_date': start_formatted_date,
            'end_date': end_formatted_date,
            'week': request.data.get('week'),
            'release_date': release_formatted_date,
            'album': request.data.get('album'),
            'youtube_id': request.data.get('youtube_id'),
            'profile': user
        }
        

        # Create the song
        song = Song.objects.create(**song_info)
        # Add the artists to the song
        song.artists.set(artists_ids)

        serializer = self.get_serializer(song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# get the last week added to the songs to user
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def last_week(request):
    if Song.objects.filter(profile=request.user).exists():
        last_song = Song.objects.filter(profile=request.user).latest('id')
        week = last_song.week + 1
    else:
        week = 1
    
    return Response({'week': week})