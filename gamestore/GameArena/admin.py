from django.contrib import admin
from .models import Game, GameState, Score, Category

admin.site.register(Game)
admin.site.register(GameState)
admin.site.register(Score)
admin.site.register(Category)
