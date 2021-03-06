# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-13 16:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0027_auto_20161007_2111'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='avatar',
            options={'verbose_name': 'Avatar', 'verbose_name_plural': 'Avatars'},
        ),
        migrations.AlterModelOptions(
            name='cv',
            options={'verbose_name': 'Curriculum Vitae', 'verbose_name_plural': 'Curriculum Vitae'},
        ),
        migrations.AlterModelOptions(
            name='programmejobrelation',
            options={'verbose_name': 'Programme-Job-Relation', 'verbose_name_plural': 'Programme-Job-Relations'},
        ),
        migrations.AlterModelOptions(
            name='signature',
            options={'verbose_name': 'Signature', 'verbose_name_plural': 'Signatures'},
        ),
        migrations.AlterModelOptions(
            name='studentjobrelation',
            options={'verbose_name': 'Student-Job-Relation', 'verbose_name_plural': 'Students-Job-Relations'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'User Profile', 'verbose_name_plural': 'User Profiles'},
        ),
    ]
