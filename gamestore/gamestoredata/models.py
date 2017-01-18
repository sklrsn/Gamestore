from django.db import models
from django.contrib.auth.models import User
from .usertypes import USER_CHOICES
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = CloudinaryField('picture', blank=True)
    user_type = models.CharField(max_length=1, choices=USER_CHOICES, default='P')

    class Meta:
        db_table = "UserProfile"

    def __str__(self):
        return self.user.username


class Game(models.Model):
    name = models.TextField(help_text="Please specify your game name")
    description = models.TextField(max_length=250)
    logo = CloudinaryField('logo', blank=True)
    uri = models.URLField(help_text="Please specify the URL")
    cost = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Game"

    def __str__(self):
        return self.name


class Purchase(models.Model):
    cost = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Purchase"

    def __str__(self):
        return self.purchase_date


class Score(models.Model):
    last_played = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Score"

    def __str__(self):
        self.last_played


class GameState(models.Model):
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "State"

    def __str__(self):
        return self.last_modified
