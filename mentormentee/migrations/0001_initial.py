# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchProposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alum_current_institute', models.TextField(null=True, verbose_name=b'Alumni Current Institute', blank=True)),
                ('alum_current_address', models.TextField(null=True, verbose_name=b'Alumni Address', blank=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('duration', models.DecimalField(null=True, verbose_name=b'Duration in Months', max_digits=4, decimal_places=2, blank=True)),
                ('hours_week', models.DecimalField(null=True, verbose_name=b'Estimated Hours/Week', max_digits=3, decimal_places=1, blank=True)),
                ('prerequsites', models.TextField(max_length=200, null=True, blank=True)),
                ('outcome', models.TextField(max_length=200, null=True, blank=True)),
                ('added', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('last_updated', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_on', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('alum_owner', models.ForeignKey(blank=True, to='jobportal.Alumni', null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StudentProposalRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('writeup', models.TextField(max_length=500)),
                ('max_hours', models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True)),
                ('opt_out', models.BooleanField(default=False)),
                ('opt_out_date', models.DateTimeField(null=True, blank=True)),
                ('date_applied', models.DateTimeField(null=True, blank=True)),
                ('report_byAlum', models.BooleanField(default=False)),
                ('report_byAlum_reasons', models.TextField()),
                ('report_byAlum_date', models.DateField(null=True, blank=True)),
                ('report_byStud', models.BooleanField(default=False)),
                ('report_byStud_reasons', models.TextField()),
                ('report_byStud_date', models.DateField(null=True, blank=True)),
                ('proposal', models.ForeignKey(to='mentormentee.ResearchProposal', null=True)),
                ('stud', models.ForeignKey(blank=True, to='jobportal.Student', null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='researchproposal',
            name='applicants',
            field=models.ManyToManyField(to='jobportal.Student', through='mentormentee.StudentProposalRelation'),
        ),
    ]
