# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0025_job_progs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='progs',
        ),
    ]
