from django.contrib import admin
from django.urls import path
from sales_list import views as sales

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', sales.home, name='home'),
]
