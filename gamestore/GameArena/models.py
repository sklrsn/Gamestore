from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "Category"
        ordering = ['name']

    def __str__(self):
        return self.name


# model to store game uploads
class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    logo = models.URLField()
    resource_info = models.URLField()
    cost = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    modified_date = models.DateTimeField(auto_now_add=True)
    developer_info = models.ForeignKey(User, related_name='uploaded_games', on_delete=models.CASCADE)
    game_category = models.ForeignKey(Category, related_name='games_category')

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

    def shortdesc(self):
        if len(self.description) > 100:
            return self.description[:100] + "..."
        return self.description

    def __str__(self):
        return self.name


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
            score=self.score,
            date_played = self.last_played)

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

class Plays(models.Model):
    game = models.ForeignKey(Game, related_name='game_played', on_delete=models.CASCADE)
    player = models.ForeignKey(User, related_name='player_plays', on_delete=models.CASCADE)
    played_on = models.DateTimeField(auto_now=True)
    def as_json_dict(self):
        return dict(
            player=self.player.username,
            game=self.game.id,
            date_played = self.played_on)
    class Meta:
        db_table = "GamePlays"
        ordering = ['played_on']
    def __str__(self):
        return self.last_modified
