# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0005_auto_20160606_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='sent_back',
        ),
    ]
