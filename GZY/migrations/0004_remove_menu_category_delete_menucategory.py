# Generated by Django 5.0 on 2023-12-18 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GZY', '0003_alter_menu_visible_alter_menucategory_visible'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='category',
        ),
        migrations.DeleteModel(
            name='MenuCategory',
        ),
    ]
