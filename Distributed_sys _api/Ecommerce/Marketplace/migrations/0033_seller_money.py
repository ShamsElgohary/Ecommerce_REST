# Generated by Django 3.2.9 on 2021-12-06 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Marketplace', '0032_customer_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='money',
            field=models.IntegerField(default=30),
        ),
    ]
