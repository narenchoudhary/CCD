# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-06 04:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0073_auto_20160805_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='fee_transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Fee Transaction ID'),
        ),
    ]
