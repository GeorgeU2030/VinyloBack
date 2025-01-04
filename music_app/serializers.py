from rest_framework import serializers
from .models import Song, Artist, Award, Ranking


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class RankingSerializer(serializers.ModelSerializer):
    musician = ArtistSerializer()
    class Meta:
        model = Ranking
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True)

    class Meta:
        model = Song
        fields = '__all__'