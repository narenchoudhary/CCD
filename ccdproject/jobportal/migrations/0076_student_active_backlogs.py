# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-10 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0075_auto_20160810_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='active_backlogs',
            field=models.IntegerField(default=0, verbose_name=b'Number of active backlogs'),
        ),
    ]