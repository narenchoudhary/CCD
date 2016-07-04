# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0008_company_signup_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='approved',
            field=models.NullBooleanField(default=None),
        ),
    ]
