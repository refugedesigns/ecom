from django.contrib import admin
from .models import Product, Address, OrderItem, Order, Payment


class ProductAdmin(admin.ModelAdmin):
    fields = ("title", "slug", "description", "active",)
    list_display = ['title', 'created', 'updated', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['title']

    
admin.site.register(Payment)
admin.site.register(Address)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)


