from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^change_password/$', views.change_password, name='update_password'),
    url(r'^update_profile/$', views.update_profile, name='update_profile'),
    url(r'^register_user/$', views.register_user, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^home/$', views.home, name='home'),
    url(r'^index/$', views.index, name='index'),
    url(r'^upload_game/$', views.upload_game, name='upload_game'),
    url(r'^edit_game/(?P<game_id>[0-9]+)/$', views.edit_game, name='edit_game'),
    url(r'^$', views.index, name='index'),
    url(r'^player/(?P<game_id>[0-9]+)/$', views.play_game, name='play_game'),
]
