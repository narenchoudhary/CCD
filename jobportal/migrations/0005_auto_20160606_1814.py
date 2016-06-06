# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0004_job_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='application_deadline',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='opening_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='posted_by_alumnus',
            field=models.NullBooleanField(default=False, verbose_name=b'Posted by Alum'),
        ),
        migrations.AlterField(
            model_name='job',
            name='posted_by_company',
            field=models.NullBooleanField(default=False, verbose_name=b'Posted by Company'),
        ),
    ]
