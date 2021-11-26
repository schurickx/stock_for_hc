from django.contrib import admin
from .models import *


@admin.register(Position)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'unit', 'provider', 'category')
    search_fields = ('title', 'provider')
    list_editable = ('title',)
    list_filter = ('title', 'provider')


@admin.register(Invoice)
class InvoicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'shipping_date', 'title', 'provider', 'create_date')
    search_fields = ('title', 'shipping_date', 'provider',)
    list_editable = ('shipping_date', 'provider',)
    list_filter = ('provider', 'shipping_date')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'quantity', 'price', 'price_sum',)
    search_fields = ('position', 'entity', 'invoice')
    list_filter = ('entity', 'invoice')


@admin.register(OperationDetail)
class OperationDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'operation', 'position', 'quantity', 'price', 'price_sum',)
    search_fields = ('position', 'entity', 'invoice')
    list_filter = ('entity', 'operation', )


admin.site.register(Category)
admin.site.register(Provider)
admin.site.register(Entity)
admin.site.register(Operation)
admin.site.site_header = 'Складской учёт'
