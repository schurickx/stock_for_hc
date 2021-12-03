from django.contrib import admin
from .models import *


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'unit', 'provider', 'category')
    list_display_links = ('title',)
    search_fields = ('title', 'provider')
    # list_editable = ('title',)
    list_filter = ('provider', 'category')


@admin.register(Invoice)
class InvoicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'shipping_date', 'title', 'provider', 'create_date')
    list_display_links = ('title',)
    search_fields = ('title', 'shipping_date', 'provider',)
    # list_editable = ('shipping_date', 'provider',)
    list_filter = ('provider', 'shipping_date')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'entity', 'invoice', 'price', )
    list_display_links = ('id', 'position',)
    search_fields = ('position', 'entity', 'invoice')
    list_filter = ('entity', 'invoice')


@admin.register(OperationDetail)
class OperationDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'operation', 'stock', 'quantity', 'comment', )
    search_fields = ('operation', 'stock', )


admin.site.register(Category)
admin.site.register(Provider)
admin.site.register(Entity)
admin.site.register(Operation)
admin.site.site_header = 'Складской учёт'
