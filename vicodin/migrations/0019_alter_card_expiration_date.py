# Generated by Django 5.0.7 on 2024-08-01 14:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vicodin', '0018_alter_card_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiration_date',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Date must be in YYYY-MM format', regex='^\\d{4}-\\d{2}$')]),
        ),
    ]
