# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-17 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0086_auto_20160817_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='discipline',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]