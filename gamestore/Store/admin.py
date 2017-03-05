from django.contrib import admin
from .models import Purchase, Order, Cart

admin.site.register(Purchase)
admin.site.register(Order)
admin.site.register(Cart)
