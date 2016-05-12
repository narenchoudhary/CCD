# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0034_auto_20160408_0959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumjobrelation',
            name='alum',
        ),
        migrations.RemoveField(
            model_name='alumjobrelation',
            name='job',
        ),
        migrations.DeleteModel(
            name='AlumJobRelation',
        ),
    ]
