from django.contrib import admin
from .models import Category, Product, Size

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Size)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'normal_price', 'discount_price', 'flash_sale_start', 'flash_sale_end']
    list_editable = ['normal_price', 'discount_price', 'flash_sale_start', 'flash_sale_end']
    search_fields = ['name']

# admin.site.register(Category)