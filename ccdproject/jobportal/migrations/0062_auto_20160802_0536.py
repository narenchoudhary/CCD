# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-02 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0061_auto_20160802_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='head_hr_mobile',
            field=models.CharField(max_length=12, null=True, verbose_name=b'Head HR Mobile'),
        ),
    ]