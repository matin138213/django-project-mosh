from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

from core.models import User
from tags.models import TagItem
from store.admin import ProductAdmin
from store.models import Product
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2",'firs_name','last_name'),
            },
        ),
    )


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TagItem
    ct_field = 'content_type'
    fk_name = 'object_id'


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
