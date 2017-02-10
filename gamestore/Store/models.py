from django.db import models
from django.contrib.auth.models import User
from GameArena.models import Game
import datetime

# Purchase information
class Purchase(models.Model):
    game_details = models.ForeignKey(Game, related_name='purchased_games', on_delete=models.CASCADE)
    player_details = models.ForeignKey(User, related_name='purchased_players', on_delete=models.CASCADE)
    cost = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    purchase_date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    class Meta:
        db_table = "Purchase"
        ordering = ['purchase_date']
    def shortdesc(self):
        if(len(self.game_details.description)>100):
            return self.game_details.description[0:100]+"..."
        else:
            return self.game_details.description
    def __str__(self):
        return self.game_details.name
