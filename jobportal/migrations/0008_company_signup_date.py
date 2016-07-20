# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0007_auto_20160606_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='signup_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
