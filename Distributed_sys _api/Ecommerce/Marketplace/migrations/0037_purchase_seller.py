# Generated by Django 2.2.24 on 2021-12-28 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Marketplace', '0036_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='seller',
            field=models.IntegerField(null=True),
        ),
    ]
