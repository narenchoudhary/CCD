# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0002_auto_20160605_1305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='password_copy',
        ),
    ]
