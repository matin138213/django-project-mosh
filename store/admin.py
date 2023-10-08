from django.contrib import admin, messages
from django.db.models import Count, Value, QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode
from tags.models import TagItem
from . import models


# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
                reverse('admin:store_product_changelist')
                + '?'
                + urlencode({'collection__id': str(collection.id)
                             }))

        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return
        return queryset.filter(inventory__lt=10)





@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title'],
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['order']
    list_filter = ['collection', 'last_update', InventoryFilter]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

    @admin.action(description='clear inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)

        self.message_user(
            request,
            f'{update_count}product were succesfuly update',
            messages.ERROR
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name__startswith', 'last_name__startswith']

    @admin.display(ordering='order_count')
    def order_count(self, order):
        url = (
                reverse('admin:store_order_changelist')
                + '?'
                + urlencode({'order__id': str(order.id)
                             }))

        return format_html('<a href="{}">{}</a>', url, order.order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count=Count('order')
        )


class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'place_at', 'customer']
