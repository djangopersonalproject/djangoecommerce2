# Generated by Django 5.1.4 on 2025-01-01 03:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
