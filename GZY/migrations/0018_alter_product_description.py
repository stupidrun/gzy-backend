# Generated by Django 5.0 on 2023-12-20 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GZY', '0017_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
