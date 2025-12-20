from django.contrib import admin
from .models import Product
from .models import Order, OrderItem
# Register your models here.
admin.site.register(Product)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'email',
        'phone',
        'total_price',
        'paid',
        'created_at'
    )

    list_filter = ('paid', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    ordering = ('-created_at',)

    inlines = [OrderItemInline]

    readonly_fields = ('total_price', 'created_at')

    fieldsets = (
        ('Customer Info', {
            'fields': ('full_name', 'email', 'phone', 'address')
        }),
        ('Order Info', {
            'fields': ('total_price', 'paid', 'created_at')
        }),
    )
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'order', 'price', 'quantity')
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ('product_name', 'price', 'quantity')