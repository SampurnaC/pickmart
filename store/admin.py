from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(Order)
# admin.site.register(OrderItem)
admin.site.register(Cart)

class OrderItemInline(admin.TabularInline):
    model=OrderItem
    # raw_id_fields=["product"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display=["id", "product", "quantity"]
    inlines=[OrderItemInline]
