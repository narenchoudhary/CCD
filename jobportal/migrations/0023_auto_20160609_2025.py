# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0022_auto_20160609_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentjobrelation',
            name='dropped_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='studentjobrelation',
            name='placed_approved_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='studentjobrelation',
            name='placed_init_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='studentjobrelation',
            name='shortlist_approved_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='studentjobrelation',
            name='shortlist_init_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
