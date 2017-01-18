from django.contrib import admin
from .models import UserProfile, Game, Purchase, ScoreBoard, GameState

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Purchase)
admin.site.register(ScoreBoard)
admin.site.register(GameState)
