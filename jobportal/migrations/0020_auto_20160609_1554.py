# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0019_auto_20160609_0022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programmejobrelation',
            name='dept',
        ),
        migrations.RemoveField(
            model_name='programmejobrelation',
            name='year',
        ),
    ]
