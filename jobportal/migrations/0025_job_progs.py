# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0024_auto_20160610_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='progs',
            field=models.ManyToManyField(to='jobportal.Programme'),
        ),
    ]
