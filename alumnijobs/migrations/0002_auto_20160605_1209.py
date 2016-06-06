# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0001_initial'),
        ('alumnijobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumjobrelation',
            name='alum',
            field=models.ForeignKey(blank=True, to='jobportal.Alumni', null=True),
        ),
        migrations.AddField(
            model_name='alumjobrelation',
            name='job',
            field=models.ForeignKey(blank=True, to='alumnijobs.AlumJob', null=True),
        ),
        migrations.AddField(
            model_name='alumjob',
            name='company_owner',
            field=models.ForeignKey(to='jobportal.Company'),
        ),
    ]
