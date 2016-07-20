# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0020_auto_20160609_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmejobrelation',
            name='dept',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'year', to='jobportal.Department', chained_field=b'year', null=True),
        ),
        migrations.AddField(
            model_name='programmejobrelation',
            name='year',
            field=models.ForeignKey(to='jobportal.Year', null=True),
        ),
    ]
