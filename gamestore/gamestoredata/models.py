from django.db import models
from django.contrib.auth.models import User
from gamestoreui.usertypes import USER_CHOICES
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = CloudinaryField('picture', blank=True)
    usertype = models.CharField(max_length=1, choices=USER_CHOICES, default='P')

    class Meta:
        db_table = "UserProfile"

    def __str__(self):
        return self.user.username
