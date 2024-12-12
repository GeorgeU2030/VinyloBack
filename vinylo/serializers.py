from rest_framework import serializers
from music_app.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "password", "email", "avatar", "year"]
