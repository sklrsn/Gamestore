from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addtocart/$', views.add_to_cart, name='addtocart'),
    url(r'^remvoefromcart/$', views.remove_from_cart, name='removefromcart'),
    url(r'^cart/$', views.get_cart, name='getcart'),
    url(r'^purchase/$', views.purchase, name='purchase'),
    url(r'^paymentsuccess/$', views.purchase_response, name='payment_success'),
    url(r'^paymentcancel/$', views.purchase_response, name='payment_cancel'),
    url(r'^paymentfailure/$', views.purchase_response, name='payment_failure'),
]
