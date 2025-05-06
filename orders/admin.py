from django.contrib import admin
from inventory.models import Drug
from .models import (
    Drug,
    Order
    
)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'drug', 'quantity')
    search_fields = ('customer_name', 'drug')
    list_filter = ['drug']

    



admin.site.register(Order,OrderAdmin)
