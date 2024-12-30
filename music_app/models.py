from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# Model for user with the following fields:
class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.TextField(default="https://www.freeiconspng.com/uploads/am-a-19-year-old-multimedia-artist-student-from-manila--21.png")
    year = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    date_init = models.CharField(null=True, blank=True)
    current_date = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.email}"

# Model for award , it has the type of award, the points and the year
class Award(models.Model):
    description = models.CharField(max_length=255, null=False, blank=False)
    # 1 - song 
    # 2 - month
    # 3 - semester 1
    # 4 - semester 2
    # 5 - year
    type_award = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    year = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.description}"

# Model for artist with the following fields:
class Artist(models.Model):
    name = models.CharField(max_length=100)
    photo = models.TextField()
    flag = models.TextField()
    country = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    genres = models.CharField(max_length=100)
    rating = models.FloatField(default=0)
    best_position = models.IntegerField(default=0)
    current_position = models.IntegerField(default=99999)
    start_date_best_position = models.DateField(null=True)
    end_date_best_position = models.DateField(null=True)
    points_year = models.IntegerField(default=0)
    points_semester = models.IntegerField(default=0)
    awards = models.ManyToManyField(Award, related_name="artists", blank=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

# Model for song with the following fields, it could have many artists:
class Song(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    rating = models.FloatField(null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    week = models.IntegerField(default=0)
    release_date = models.DateField(null=False, blank=False)
    album = models.CharField(null=False, blank=False)
    youtube_id = models.CharField(max_length=255, null=False, blank=False)
    artists = models.ManyToManyField(Artist, related_name="songs")
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


# Model for rank is for the weekly ranking of the artists
class Rank(models.Model):
    week = models.IntegerField()
    position = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.week}"


# Model for ranking is for semester and yearly ranking of the artists it saves the points in that period
class Ranking(models.Model):
    period = models.CharField(max_length=50)
    points = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ranking {self.period}"