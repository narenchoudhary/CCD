# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0006_remove_job_sent_back'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='posted_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
