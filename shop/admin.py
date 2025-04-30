# shop/admin.py

from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'normal_price', 'discount_price', 'flash_sale_start', 'flash_sale_end']
    list_editable = ['normal_price', 'discount_price', 'flash_sale_start', 'flash_sale_end']
    search_fields = ['name']