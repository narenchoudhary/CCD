# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-25 01:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0052_auto_20160725_0628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='bond',
        ),
    ]