from django.contrib import admin
from . import models


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'visible',
        'created_at',
    )
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        'alt_text',
        'url',
        'created_at',
        'visible',
    )
    list_filter = (
        'visible',
    )


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CustomPage)
class CustomPageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProductDetailImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'image',
        'index',
        'visible',
        'created_at',
    )
    list_editable = (
        'index',
        'visible',
    )
    list_filter = (
        'visible',
    )
