from django.contrib import admin
from .models import *


@admin.register(Positions)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'unit', 'provider', 'category')
    search_fields = ('title', 'provider')
    list_editable = ('title',)
    list_filter = ('title', 'provider')


@admin.register(Invoices)
class InvoicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'shipping_date', 'title', 'provider', 'create_date')
    search_fields = ('title', 'shipping_date')
    list_editable = ('title', 'shipping_date')
    list_filter = ('title', 'provider', 'shipping_date')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'quantity', 'price', 'price_sum',)
    search_fields = ('position', 'entity', 'invoice')
    list_filter = ('position', 'entity', 'invoice')


@admin.register(OperationDetail)
class OperationDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'operation', 'position', 'quantity', 'price', 'price_sum',)
    search_fields = ('position', 'entity', 'invoice')
    list_filter = ('position', 'entity', 'invoice')


admin.site.register(Categories)
admin.site.register(Providers)
admin.site.register(Entity)
admin.site.register(Operations)
admin.site.site_header = 'Складской учёт'
