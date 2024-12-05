from django.contrib import admin
from .models import MenuItem, OrderDetail, OrderSummary
# Register your models here.

admin.site.register(MenuItem)
admin.site.register(OrderSummary)
admin.site.register(OrderDetail)
