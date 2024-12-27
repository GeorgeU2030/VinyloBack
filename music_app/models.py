from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.TextField(default="https://www.freeiconspng.com/uploads/am-a-19-year-old-multimedia-artist-student-from-manila--21.png")
    year = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    date_init = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.email}"
