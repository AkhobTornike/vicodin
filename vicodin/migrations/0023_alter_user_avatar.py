# Generated by Django 5.0.7 on 2024-08-04 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vicodin', '0022_remove_order_cart_order_price_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to='users_images/'),
        ),
    ]
