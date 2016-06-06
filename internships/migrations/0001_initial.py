# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IndInternship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('designation', models.CharField(max_length=20)),
                ('profile', models.CharField(max_length=10)),
                ('stipend', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('posted_on', models.DateTimeField()),
                ('last_updated', models.DateTimeField()),
                ('approved', models.NullBooleanField(default=None)),
                ('approved_on', models.DateTimeField(null=True)),
                ('opening_date', models.DateTimeField()),
                ('closing_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammeInternRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentInternRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round', models.IntegerField(default=1)),
                ('shortlist_init', models.BooleanField(default=False)),
                ('shortlist_approved', models.NullBooleanField(default=None)),
                ('intern_init', models.BooleanField(default=False)),
                ('intern_approved', models.NullBooleanField(default=None)),
                ('ppo_init', models.BooleanField(default=False)),
                ('ppo_approved', models.NullBooleanField(default=None)),
                ('dropped', models.BooleanField(default=False)),
                ('cv1', models.BooleanField(default=False)),
                ('cv2', models.BooleanField(default=False)),
                ('intern', models.ForeignKey(to='internships.IndInternship')),
            ],
        ),
    ]
