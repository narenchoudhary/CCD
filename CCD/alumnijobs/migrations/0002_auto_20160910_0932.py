# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-10 04:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobportal', '0001_initial'),
        ('alumnijobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumjobrelation',
            name='alum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Alumni'),
        ),
        migrations.AddField(
            model_name='alumjobrelation',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alumnijobs.AlumJob'),
        ),
        migrations.AddField(
            model_name='alumjob',
            name='company_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportal.Company'),
        ),
    ]
