# Generated by Django 5.0.7 on 2024-08-02 11:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vicodin', '0020_order_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vicodin.address'),
            preserve_default=False,
        ),
    ]
