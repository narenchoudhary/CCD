# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 00:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0065_auto_20160802_2047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentjobrelation',
            name='dropped',
        ),
        migrations.RemoveField(
            model_name='studentjobrelation',
            name='dropped_date',
        ),
        migrations.RemoveField(
            model_name='studentjobrelation',
            name='round',
        ),
        migrations.RemoveField(
            model_name='studentjobrelation',
            name='shortlist_approved',
        ),
        migrations.RemoveField(
            model_name='studentjobrelation',
            name='shortlist_approved_date',
        ),
    ]
