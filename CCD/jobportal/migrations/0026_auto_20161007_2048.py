# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-07 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0025_auto_20161007_2035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programme',
            name='Year of passing',
        ),
        migrations.AddField(
            model_name='programme',
            name='year_passing',
            field=models.IntegerField(default=2017, null=True, verbose_name=b'Year of passing'),
        ),
    ]
