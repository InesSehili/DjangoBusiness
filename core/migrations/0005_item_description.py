# Generated by Django 2.2 on 2022-05-22 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='this is a short description for this item !!'),
            preserve_default=False,
        ),
    ]
