# Generated by Django 2.2.24 on 2021-12-28 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Marketplace', '0035_auto_20211228_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
