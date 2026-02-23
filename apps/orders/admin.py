from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items"""
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin"""
    list_display = ['order_id', 'user', 'full_name', 'total_amount', 'status', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['order_id', 'user__username', 'full_name', 'email']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['order_id', 'created_at', 'updated_at', 'paid_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'user', 'status', 'total_amount')
        }),
        ('Shipping Details', {
            'fields': ('full_name', 'email', 'phone', 'address', 'city', 'state', 'pincode')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'is_paid', 'paid_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
