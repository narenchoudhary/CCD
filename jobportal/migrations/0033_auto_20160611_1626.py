# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-11 10:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0032_auto_20160610_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='stud',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Student'),
        ),
        migrations.AlterField(
            model_name='cv',
            name='stud',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Student'),
        ),
        migrations.AlterField(
            model_name='signature',
            name='stud',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Student'),
        ),
    ]