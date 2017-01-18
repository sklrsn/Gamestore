from django.contrib import admin
from .models import UserProfile, Game, Purchase, Score, GameState

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Purchase)
admin.site.register(Score)
admin.site.register(GameState)
