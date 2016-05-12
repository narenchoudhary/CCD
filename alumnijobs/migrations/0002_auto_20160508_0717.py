# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnijobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumjob',
            name='approved_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
