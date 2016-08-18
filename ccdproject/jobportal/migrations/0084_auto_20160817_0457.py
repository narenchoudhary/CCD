# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-16 23:27
from __future__ import unicode_literals

from django.db import migrations, models
import jobportal.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0083_auto_20160816_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='dept',
            field=models.CharField(max_length=75),
        ),
        migrations.AlterField(
            model_name='job',
            name='bond_link',
            field=models.FileField(blank=True, null=True, upload_to=jobportal.models.get_bond_link_name, verbose_name=b'Legal Bond Document'),
        ),
    ]