# Generated by Django 3.1.4 on 2020-12-03 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_address_order_orderitem_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ImageField(blank=True, upload_to='product_images'),
        ),
    ]
