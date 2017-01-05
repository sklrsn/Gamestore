from django.db import models
from django.contrib.auth.models import User
from gamestoreui.usertypes import USER_CHOICES


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    usertype = models.CharField(max_length=1, choices=USER_CHOICES, default='P')

    class Meta:
        db_table = "UserProfile"

    def __str__(self):
        return self.user.username
