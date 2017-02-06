from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^player/(?P<game_id>[0-9]+)/$', views.play_game, name='play_game'),
    url(r'^listgames/$', views.listgames, name='listgames'),
    url(r'fb_redirect/$', views.fb_redirect, name='fb_redirect'),
]
