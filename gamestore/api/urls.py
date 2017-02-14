from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.versions, name='versions'),
    url(r'^v1/', include('api.v1.urls')),
]
