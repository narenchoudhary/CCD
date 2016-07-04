# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0009_auto_20160607_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='approved_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
