from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^store_game_score.json$', views.store_game_score, name='store_game_score'),
    url(r'^load_game_score.json$', views.load_game_score, name='load_game_score'),

    url(r'^store_game_state.json$', views.store_game_state, name='store_game_state'),
    url(r'^load_game_state.json$', views.load_game_state, name='load_game_state'),

    url(r'^store_system_configs.json$', views.store_system_configs, name='store_system_configs'),
    url(r'^load_system_configs.json$', views.load_system_configs, name='load_system_configs'),

]
