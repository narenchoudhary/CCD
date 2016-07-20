# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0018_event_creation_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='time_event',
            new_name='event_time',
        ),
    ]
