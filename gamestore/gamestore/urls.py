"""Online Game store URL Configuration"""

from django.conf.urls import url, include
from django.contrib import admin
from Users import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include('Users.urls')),
    url(r'^game/', include('GameArena.urls')),
    url(r'^accounts/', views.index, name='index'),
    url(r'^', include('Users.urls')),
]
