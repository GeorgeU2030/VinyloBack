from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from music_app.models import Artist, User, Award, Rank, Ranking
from datetime import datetime

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_artist(request):
    
    # get the week for add the award
    week = request.data.get('week')

    # get the start and end date and fortmated for the best position
    start_date_str_format = request.data.get("start_date")
    end_date_str_format = request.data.get("end_date")

    start_date = datetime.strptime(start_date_str_format, "%Y-%m-%dT%H:%M:%S.%fZ")
    end_date = datetime.strptime(end_date_str_format, "%Y-%m-%dT%H:%M:%S.%fZ")

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # get the artists for update the information
    artist_data = request.data.get('artists')

    # get the points for add to the artist
    points_for_add = request.data.get('rating')
    for artist_data in artist_data:
        # get every artist and update the points
        artist = Artist.objects.filter(name=artist_data['name'], profile=request.user)

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
        week_awards = Award.objects.filter(type_award=1)
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
            description=f"Ambar award {period}",
            points=10,
            year=award_year
        )

        first_artist.awards.add(award)

        for artist in top_10_musicians:
            Ranking.objects.create(
                artist=artist,
                period=period,
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
            description=f"Gold award {year}",
            points=30,
            year=award_year
        )

        first_artist_year.awards.add(award)

        for artist in top_10_musicians_year:
            Ranking.objects.create(
                artist=artist,
                period=year_period,
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
            description=f"Ambar award {period}",
            points=10,
            year=award_year
        )

        first_artist.awards.add(award)

        for artist in top_10_musicians:
            Ranking.objects.create(
                artist=artist,
                period=period,
                points=artist.points_semester,
                profile=request.user
            )


        return Response({'message': 'The artists have been updated'}, status=status.HTTP_200_OK)