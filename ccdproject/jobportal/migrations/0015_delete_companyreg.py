# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0014_auto_20160607_1901'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CompanyReg',
        ),
    ]
