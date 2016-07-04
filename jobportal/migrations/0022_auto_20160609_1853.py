# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0021_auto_20160609_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='open_for_internship',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='programme',
            name='open_for_placement',
            field=models.BooleanField(default=False),
        ),
    ]
