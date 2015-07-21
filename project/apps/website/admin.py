from django.contrib import admin

from .models import (
    Primitive,
    Collection,
    Duplicate,
)


@admin.register(Primitive)
class PrimitiveAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(Duplicate)
class DuplicateAdmin(admin.ModelAdmin):
    save_on_top = True
