# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnijobs', '0002_auto_20160508_0717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumjobrelation',
            name='placed_approved',
        ),
    ]
