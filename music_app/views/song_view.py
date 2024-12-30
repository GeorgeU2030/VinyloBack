from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from music_app.models import Song


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