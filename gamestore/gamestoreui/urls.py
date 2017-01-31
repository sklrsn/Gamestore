from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^manage_profile/$', views.manage_profile, name='manage_profile'),
    url(r'^register_user/$', views.register_user, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^home/$', views.home, name='home'),
    url(r'^index/$', views.index, name='index'),
    url(r'^upload_game/$', views.upload_game, name='upload_game'),
    url(r'^edit_game/(?P<game_id>[0-9]+)/$', views.edit_game, name='edit_game'),
    url(r'^$', views.index, name='index'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^player/(?P<game_id>[0-9]+)/$', views.play_game, name='play_game'),
    url(r'^listgames/$', views.listgames, name='listgames'),    
]
