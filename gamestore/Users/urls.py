from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^activate/(?P<activation_code>[a-zA-Z0-9\-]{36})/$', views.activate, name='activate'),
    url(r'^manage_profile/$', views.manage_profile, name='manage_profile'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^forgot_password/$', views.forgot_password, name='forgot_password'),
    url(r'^home/$', views.home, name='home'),
    url(r'^upload_game/$', views.upload_game, name='upload_game'),
    url(r'^edit_game/(?P<game_id>[0-9]+)/$', views.edit_game, name='edit_game'),
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^terms/$', views.terms_conditions, name='terms'),
    url(r'^downloads/$', views.download_statistics, name='download_statistics'),
]
