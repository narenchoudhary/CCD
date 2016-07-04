# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0017_studentjobrelation_creation_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='creation_datetime',
            field=models.DateTimeField(null=True, editable=False),
        ),
    ]
