"""Online Game store URL Configuration"""

from django.conf.urls import url, include
from django.contrib import admin
from gamestoreui import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^data/', include('gamestoredata.urls')),
    url(r'^profile/', include('gamestoreui.urls')),
    url(r'^accounts/', views.index, name='index'),
    url(r'^', include('gamestoreui.urls')),
]
