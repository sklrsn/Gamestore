from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.update_profile, name='update_profile'),
]
