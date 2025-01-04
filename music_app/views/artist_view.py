from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from music_app.models import Artist, User, Award, Rank, Ranking, Song
from datetime import datetime
from calendar import monthrange
from django.db.models import Q, Count
from music_app.serializers import ArtistSerializer, AwardSerializer, RankingSerializer

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_artist(request):
    
    # get the week for add the award
    week = request.data.get('week')

    # get the start and end date and fortmated for the best position
    start_date_str_format = request.data.get("start_date")
    end_date_str_format = request.data.get("end_date")

    start_date = datetime.strptime(start_date_str_format, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str_format, "%Y-%m-%d")

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # get the artists for update the information
    artist_data = request.data.get('artists')

    # get the points for add to the artist
    points_for_add = int(request.data.get('rating'))
    total_points = 0
    for artist_data in artist_data:
        # get every artist and update the points, get for unique instance
        artist = Artist.objects.get(name=artist_data['name'], profile=request.user)

        # update every point item for the artist 
        artist.points += points_for_add
        artist.points_semester += points_for_add
        artist.points_year += points_for_add
        artist.save()
        
        # add the week award for every artist

        award = Award.objects.create(
            type_award=1,
            description=f"Bronze award {week}",
            points=points_for_add,
        )

        artist.awards.add(award)

        # get the total points for the artist
        week_awards = artist.awards.filter(type_award=1)
        total_points += sum([award.points for award in week_awards])
        
        # get the rating for the artist and update it
        rating = total_points / len(week_awards) if week_awards else 0

        artist.rating = rating
        artist.save()

    # Order the artist for the ranking and ranks

    artists = Artist.objects.filter(profile=request.user)
    artists_sorted = sorted(artists, key=lambda artist_x: artist_x.points, reverse=True)

    for position, artist in enumerate(artists_sorted, start=1):
        artist.current_position = position
        artist.save()

        # add the rank for the artist

        Rank.objects.create(
            week=week,
            position=position,
            artist=artist
        )

        if artist.best_position == 0 or artist.current_position <= artist.best_position:
            artist.best_position = artist.current_position
            artist.start_date_best_position = start_date_str
            artist.end_date_best_position = end_date_str
            artist.save()
    

    # Get the year for the period
    year = start_date.year
    type_award = 0
    if week % 52 == 0:
        if start_date.month in [10,11,12]:
            period = f"Semester 2 - {str(year)}"
            type_award = 4
            award_year = year
        elif start_date.month in [1,2,3]:
            period = f"Semester 2 - {str(year-1)}"
            type_award = 4
            award_year = year - 1
        elif start_date.month in [4,5,6,7,8,9]:
            period = f"Semester 1 - {str(year)}"
            type_award = 3
            award_year = year


        # get the top 10 musicians for the period
        top_10_musicians = Artist.objects.filter(profile=request.user).order_by('-points_semester')[:10]

        first_artist = top_10_musicians[0]

        award = Award.objects.create(
            type_award=type_award,
            description=f"Amber award {period}",
            points=10,
            year=award_year
        )

        first_artist.awards.add(award)

        for artist in top_10_musicians:
            Ranking.objects.create(
                artist=artist,
                period=f"Amber award {period}",
                points=artist.points_semester,
                profile=request.user
        )

        if start_date.month in [1,2]:
            year_period = f"Period - {str(year-1)}"
            award_year = year - 1
        elif start_date.month in [3,4,5,6,7,8,9]:
            year_period = f"Period - {str(year - 1)} - {str(year)}"
            award_year = year - 1
        elif start_date.month in [10,11,12]:
            year_period = f"Period - {str(year)}"
            award_year = year

        top_10_musicians_year = Artist.objects.filter(profile=request.user).order_by('-points_year')[:10]

        first_artist_year = top_10_musicians_year[0]

        award = Award.objects.create(
            type_award=5,
            description=f"Gold award {year_period}",
            points=50,
            year=award_year
        )

        first_artist_year.awards.add(award)

        for artist in top_10_musicians_year:
            Ranking.objects.create(
                artist=artist,
                period=f"Gold award {year_period}",
                points=artist.points_year,
                profile=request.user
            )
        
        Artist.objects.filter(profile=request.user).update(points_semester=0)
        Artist.objects.filter(profile=request.user).update(points_year=0)

        return Response({'message': 'The artists have been updated'}, status=status.HTTP_200_OK)
        
    elif week % 26 == 0:
        if start_date.month in [4,5,6,7,8,9]:
            period = f"Semester 1 - {year}"
            type_award = 3
            award_year = year
        elif start_date.month in [10,11,12]:
            period = f"Semester 2 - {year}"
            type_award = 4
            award_year = year
        elif start_date.month in [1,2,3]:
            period = f"Semester 2 - {year-1}"
            type_award = 4
            award_year = year - 1


        top_10_musicians = Artist.objects.filter(profile=request.user).order_by('-points_semester')[:10]

        first_artist = top_10_musicians[0]

        award = Award.objects.create(
            type_award=type_award,
            description=f"Amber award {period}",
            points=20,
            year=award_year
        )

        first_artist.awards.add(award)

        for artist in top_10_musicians:
            Ranking.objects.create(
                artist=artist,
                period=f"Amber award {period}",
                points=artist.points_semester,
                profile=request.user
            )

    return Response({'message': 'The artists have been updated'}, status=status.HTTP_200_OK)
    

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_current_date(request):
    new_current_date = request.data.get('currentDate')
    # update the current date for the artist
    profile = request.data.get('profile')
    user = User.objects.get(id=profile)
    user.current_date = new_current_date
    user.save()

    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'name': user.name,
        'avatar': user.avatar,
        'year': user.year,
        'dateInit': user.date_init,
        'currentDate': user.current_date
    }

    return Response({'message': 'The current date has been updated', 'user':user_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_artists_of_month(request):
    # Get dates from request
    start_date = request.data.get('start_date')
    
    # Convert strings to datetime objects
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Get the first and last day of the requested month
    first_day_of_month = start_date_obj.replace(day=1).date()
    _, last_day = monthrange(start_date_obj.year, start_date_obj.month)
    last_day_of_month = start_date_obj.replace(day=last_day).date()
    

    # Query for songs that belong to the specified month
    songs = Song.objects.filter(
        profile=request.user
    ).filter(
        Q(
            # Case 1: Song starts in the month
            Q(start_date__year=start_date_obj.year) &
            Q(start_date__month=start_date_obj.month)
        ) |
        Q(
            # Case 2: Song ends in the month
            Q(end_date__year=start_date_obj.year) &
            Q(end_date__month=start_date_obj.month)
        )
    ).distinct()
    
    # Filter songs based on the number of days in the month
    songs_in_month = []
    
    for song in songs:
        # Calculate the days that fall within the month
        song_start = max(song.start_date, first_day_of_month)
        song_end = min(song.end_date, last_day_of_month)
        
        # Calculate days in current month vs total days
        days_in_month = (song_end - song_start).days + 1
        total_days = (song.end_date - song.start_date).days + 1
        
        # Include song if majority of days fall within the month
        if days_in_month >= total_days / 2:
            songs_in_month.append(song)
    
    # Get unique artists from the filtered songs
    artists = Artist.objects.filter(songs__in=songs_in_month).distinct()
    
    # Prepare response data
    artist_data = []
    for artist in artists:
        artist_data.append({
            'id': artist.id,
            'name': artist.name,
            'photo': artist.photo,
        })
    
    return Response({
        'month': start_date_obj.strftime('%B %Y'),
        'artists': artist_data
    })


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_month_award(request):
    # Get data from request
    artist_id = request.data.get('id')
    period = request.data.get('period')

    # Get the year for the period
    year = period.split(' ')[-1]
    award_year = int(year)
    
    # Get artist and create award
    artist = Artist.objects.get(id=artist_id)
    award = Award.objects.create(
        type_award=2,
        description=f"Silver award {period}",
        points=5,
        year=award_year
    )
    
    artist.points += 5
    artist.points_year += 5
    artist.points_semester += 5
    artist.save()
    artist.awards.add(award)
    
    return Response({'message': 'The award has been added'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ranking(request):
    musicians = Artist.objects.filter(profile=request.user).order_by('current_position')
    serializer = ArtistSerializer(musicians, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ranking_awards(request):
    artists = (Artist.objects.filter(profile=request.user)
                 .annotate(award_count=Count('awards'))
                 .order_by('-award_count', 'current_position'))
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_awards_history(request):
    artists = Artist.objects.filter(profile=request.user)
    awards = Award.objects.filter(artists__in=artists, type_award__in=[2, 3, 4, 5]).order_by('-id')
    
    response = []
    for award in awards:
        award_serializer = AwardSerializer(award)
        response.append({
            'artist_name': award.artists.first().name,
            'artist_photo': award.artists.first().photo if award.artists.first().photo else None,
            'award': award_serializer.data
        })

    return Response(response)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def rankings_by_history(request, period_rank):
    rankings = Ranking.objects.filter(profile=request.user,period=period_rank).order_by('id','-points')[:10]
    serializer = RankingSerializer(rankings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def stats(request):
    artists_data = Artist.objects.filter(profile=request.user).order_by('current_position').values()

    for artist in artists_data:
        ranks = Rank.objects.filter(artist_id=artist['id']).order_by('-week').values('week', 'position')[:10]
        artist['ranks'] = {rank['week']: rank['position'] for rank in ranks}

    try:
        latest_song = Song.objects.latest('id')
        max_week = latest_song.week
    except Song.DoesNotExist:
        max_week = 0

    return Response({'artistData': list(artists_data), 'maxWeek': max_week})