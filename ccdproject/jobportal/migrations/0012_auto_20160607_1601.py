# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0011_auto_20160607_1557'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='signup_date',
            new_name='signup_datetime',
        ),
    ]
