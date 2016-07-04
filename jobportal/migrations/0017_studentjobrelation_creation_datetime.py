# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0016_auto_20160607_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentjobrelation',
            name='creation_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
