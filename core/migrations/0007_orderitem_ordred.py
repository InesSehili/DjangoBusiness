# Generated by Django 2.2 on 2022-05-22 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='ordred',
            field=models.BooleanField(default=False),
        ),
    ]