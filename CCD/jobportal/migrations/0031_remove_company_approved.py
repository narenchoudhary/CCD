# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-25 18:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0030_auto_20161025_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='approved',
        ),
    ]
