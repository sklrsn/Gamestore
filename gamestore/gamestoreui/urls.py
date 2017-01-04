from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^changepassword/$', views.change_password, name='update_password'),
    url(r'^update/$', views.update_profile, name='update_profile'),
]
