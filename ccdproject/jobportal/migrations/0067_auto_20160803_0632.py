# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 01:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0066_auto_20160803_0614'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentjobrelation',
            old_name='placed_approved_date',
            new_name='placed_approved_datetime',
        ),
        migrations.RenameField(
            model_name='studentjobrelation',
            old_name='shortlist_init_date',
            new_name='shortlist_init_datetime',
        ),
    ]