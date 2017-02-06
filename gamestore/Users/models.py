from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models

from common.constants import USER_CHOICES


# Model to Store the user details
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = CloudinaryField('picture', blank=True)
    user_type = models.CharField(max_length=1, choices=USER_CHOICES, default='P')
    activation_token = models.CharField(max_length=36, blank=True)

    class Meta:
        db_table = "UserProfile"

    def __str__(self):
        return self.user.username
