from django.db import models
from django.contrib.auth.models import User
from .constants import USER_CHOICES
from cloudinary.models import CloudinaryField
from django.core.urlresolvers import reverse


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


# model to store game uploads
class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    logo = models.URLField()
    resource_info = models.URLField()
    cost = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    modified_date = models.DateTimeField(auto_now_add=True)
    developer_info = models.ForeignKey(User, related_name='uploaded_games', on_delete=models.CASCADE)

    class Meta:
        db_table = "Game"
        ordering = ['modified_date']

    def to_json_dict(self):
        res = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'url': reverse("play_game", kwargs={'game_id': self.id}),
            'cost': self.cost,
            'modified_date': str(self.modified_date),
            'logo': self.logo
        }
        return res

    def __str__(self):
        return self.name


# Purchase information
class Purchase(models.Model):
    game_details = models.ForeignKey(Game, related_name='game_details', on_delete=models.CASCADE)
    player_details = models.ForeignKey(User, related_name='player_details', on_delete=models.CASCADE)
    cost = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Purchase"
        ordering = ['purchase_date']

    def __str__(self):
        return self.purchase_date


# store scores history
# TODO : rename player_info to player and game_info to game
class Score(models.Model):
    game_info = models.ForeignKey(Game, related_name='game_info', on_delete=models.CASCADE)
    player_info = models.ForeignKey(User, related_name='player_info', on_delete=models.CASCADE)
    last_played = models.DateTimeField(auto_now=True)
    score = models.BigIntegerField(default=0)

    def as_json_leader(self):
        return dict(
            player=self.player_info.username,
            score=self.score)

    class Meta:
        db_table = "Score"
        ordering = ['last_played']

    def __str__(self):
        self.player_info.username


# store state of the previous action
# TODO change app_state to game_state
class GameState(models.Model):
    game = models.ForeignKey(Game, related_name='game_state', on_delete=models.CASCADE)
    player = models.ForeignKey(User, related_name='player_state', on_delete=models.CASCADE)
    app_state = models.TextField(blank=True, max_length=500)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "GameState"
        ordering = ['last_modified']
        unique_together = ('game', 'player')

    def __str__(self):
        return self.last_modified
