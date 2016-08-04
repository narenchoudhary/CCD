# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0023_auto_20160609_2025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='minor_programme',
        ),
        migrations.AddField(
            model_name='student',
            name='minor_dept',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'year', related_name='minor_dept', chained_field=b'minor_year', to='jobportal.Department', null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='minor_prog',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'dept', related_name='minor_prog', chained_field=b'minor_dept', to='jobportal.Programme', null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='minor_year',
            field=models.ForeignKey(related_name='minor_year', to='jobportal.Year', null=True),
        ),
    ]
