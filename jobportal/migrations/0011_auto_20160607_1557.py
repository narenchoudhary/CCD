# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0010_company_approved_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='approved_on',
            new_name='approval_date',
        ),
    ]
