# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 01:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0067_auto_20160803_0632'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentjobrelation',
            old_name='placed_init_date',
            new_name='placed_init_datetime',
        ),
    ]
