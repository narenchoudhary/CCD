# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-05 18:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0023_auto_20161005_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentjobrelation',
            name='is_debarred',
            field=models.BooleanField(default=False),
        ),
    ]