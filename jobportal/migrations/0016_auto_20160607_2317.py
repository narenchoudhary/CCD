# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0015_delete_companyreg'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='programme',
            unique_together=set([('year', 'dept', 'name', 'minor_status')]),
        ),
    ]
