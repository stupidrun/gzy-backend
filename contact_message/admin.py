from django.contrib import admin
from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'followed',
        'created_at',
    )
    list_filter = (
        'followed',
    )
