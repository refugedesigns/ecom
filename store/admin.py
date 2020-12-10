from django.contrib import admin
from .models import Product, Address, OrderItem, Order, Payment, ColorVariation, SizeVariation, Category


class ProductAdmin(admin.ModelAdmin):
    fields = ("title", "slug", "price", "stock", "image", "description", "active", "available_colors", "available_sizes", "primary_category", "secondary_categories")
    list_display = ['title', 'created', 'updated', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['title']

class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "address_line_1", "address_line_2", "city", "zip_code", "address_type",]
    list_filter = ['default']

admin.site.register(Payment)
admin.site.register(Address, AddressAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
admin.site.register(ColorVariation)
admin.site.register(SizeVariation)
admin.site.register(Category)

