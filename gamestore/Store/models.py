from django.db import models
from django.contrib.auth.models import User
from GameArena.models import Game


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
