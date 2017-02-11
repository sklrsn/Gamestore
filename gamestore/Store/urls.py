from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addtocart/$', views.add_to_cart, name='addtocart'),
    url(r'^remvoefromcart/$', views.remove_from_cart, name='removefromcart'),
    url(r'^cart/$', views.get_cart, name='getcart'),
    url(r'^purchase/$', views.purchase, name='purchase'),
    url(r'^paymentresult/$', views.purchase_result, name='payment_result'),
]
