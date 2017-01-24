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
    url(r'^$', views.index, name='index'),
]
