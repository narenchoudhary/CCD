# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-15 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0006_auto_20160912_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitemanagement',
            name='job_stud_photo_allowed',
            field=models.BooleanField(default=False, verbose_name=b'Allow Avatar Upload for Job Candidates'),
        ),
        migrations.AddField(
            model_name='sitemanagement',
            name='job_stud_sign_allowed',
            field=models.BooleanField(default=False, verbose_name=b'Allow Sign Upload for Intern Candidates'),
        ),
    ]
