from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from tags.models import TagItem
from store.admin import ProductAdmin
from store.models import Product


# Register your models here.


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TagItem
    ct_field = 'content_type'
    fk_name = 'object_id'


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
