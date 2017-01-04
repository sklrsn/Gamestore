from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update/$', views.update_profile, name='update_profile'),
]
