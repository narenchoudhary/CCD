# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0035_auto_20160507_0324'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlumJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designation', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=200, null=True, blank=True)),
                ('profile_name', models.CharField(max_length=20)),
                ('audience', models.CharField(max_length=6, choices=[(b'young', b'Young Alumni'), (b'old', b'Older Alumni'), (b'all', b'All Alumni')])),
                ('approved', models.NullBooleanField(default=None)),
                ('approved_on', models.DateTimeField(null=True)),
                ('posted_on', models.DateTimeField()),
                ('opening_date', models.DateTimeField()),
                ('closing_date', models.DateTimeField()),
                ('company_owner', models.ForeignKey(to='jobportal.Company')),
            ],
        ),
        migrations.CreateModel(
            name='AlumJobRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('placed_init', models.BooleanField(default=False)),
                ('placed_approved', models.BooleanField(default=False)),
                ('shortlist_status', models.BooleanField(default=False)),
                ('alum', models.ForeignKey(blank=True, to='jobportal.Alumni', null=True)),
                ('job', models.ForeignKey(blank=True, to='alumnijobs.AlumJob', null=True)),
            ],
        ),
    ]
