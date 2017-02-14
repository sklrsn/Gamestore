from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^GetGame/(?P<game_id>[0-9]+)/$', views.get_game, name='GetGame'),
    url(r'^GetLeaders/(?P<game_id>[0-9]+)/$', views.get_leaders, name='GetLeaders'),
    url(r'^GetPurchases/(?P<game_id>[0-9]+)/$', views.get_purchases, name='GetPurchases'),
    url(r'^GetPlayedDetails/(?P<game_id>[0-9]+)/$', views.get_played_details, name='GetPlayedDetails'),
    url(r'^GetAllGames/$', views.get_allgames,name='GetAllGames'),
]
