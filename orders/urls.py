from django.urls import path
from .views import *

urlpatterns = [
    path('', all_orders,name='all-orders'),
    path('add-order/', add_order,name='add-order'),
    path('order/<int:pk>/edit/', edit_order,name='edit-order'),
    path('order/<int:pk>/delete/', delete_order, name='delete-order')
]
