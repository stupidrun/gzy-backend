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


@admin.register(models.SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = (
        'site_name',
        'mobile',
        'tel',
        'address',
        'email',
        'visible',
    )
    list_filter = (
        'visible',
    )

@admin.register(models.ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'visible',
        'recommend',
        'created_at',
    )
    list_filter = (
        'category',
        'visible',
    )
    list_editable = (
        'visible',
        'recommend',
    )


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CustomPage)
class CustomPageAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'banner_hidden',
        'show_in_index',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'banner_hidden',
        'show_in_index',
    )
    list_editable = (
        'banner_hidden',
        'show_in_index',
    )


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
