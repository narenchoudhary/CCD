# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-31 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0099_auto_20160831_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[(b'Screening Test', b'Screening Test'), (b'Pre Placement Talk', b'Pre Placement Talk'), (b'Workshop', b'Workshop'), (b'Promotional Event', b'Promotional Event')], help_text=b'Select event type from the dropdown menu.', max_length=30, null=True, verbose_name=b'Event Type'),
        ),
    ]
