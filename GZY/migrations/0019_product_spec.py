# Generated by Django 5.0 on 2023-12-20 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GZY', '0018_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='spec',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Spec'),
        ),
    ]
