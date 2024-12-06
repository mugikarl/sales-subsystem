from django.contrib import admin
from django.urls import path
from sales_list import views as sales

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', sales.home, name='home'),
    path('neworder/<int:order_id>/', sales.new_order, name='neworder'),
    path('create-new-order/', sales.create_new_order, name='create_new_order'),
    path('delete-order-item/<int:id>/', sales.deleteOrderItem, name='delete_order_item'),
    #path('edit-order-item/<int:id>/', sales.editOrderItem, name='edit_order_item'),
    path('update_quantity/<int:id>/', sales.update_quantity, name='update_quantity'),
    path('order/payment/<int:order_id>/', sales.process_payment, name='process_payment'),
    path('delete-order-summary/<int:id>/', sales.deleteOrderSummary, name='delete_order_summary'),
    path('menulist/', sales.menu_list, name='menu_list'),
    path('delete-menu-item/<int:id>/', sales.deleteMenuItem, name='delete_menu_item'),
    path('edit-menu-item/<int:id>/' ,sales.editMenuItem, name='edit_menu_item'),
    path('order/payment/<int:order_id>/preview/', sales.report_preview, name='report_preview'),
    path('order/payment/<int:order_id>/download/', sales.report_download, name='report_download'),
    path('order/payment/<int:order_id>/preview/', sales.report_preview, name='report_preview'),
    path('order/payment/<int:order_id>/download/', sales.report_download, name='report_download'),
]