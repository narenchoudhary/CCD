# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0013_auto_20160607_1622'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'managed': True},
        ),
        migrations.RenameField(
            model_name='event',
            old_name='final_date',
            new_name='event_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='alum_owner',
        ),
        migrations.RemoveField(
            model_name='event',
            name='date1',
        ),
        migrations.RemoveField(
            model_name='event',
            name='date2',
        ),
        migrations.RemoveField(
            model_name='event',
            name='date3',
        ),
        migrations.RemoveField(
            model_name='event',
            name='finalised',
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, max_length=30, null=True, choices=[(b'Pre Placement Talk', b'Pre Placement Talk'), (b'Workshop', b'Workshop'), (b'Promotional Event', b'Promotional Event')]),
        ),
        migrations.AddField(
            model_name='event',
            name='is_approved',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='event',
            name='time_event',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
