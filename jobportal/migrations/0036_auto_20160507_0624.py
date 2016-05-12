# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0035_auto_20160507_0324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alumni',
            options={'managed': True},
        ),
        migrations.RemoveField(
            model_name='alumni',
            name='department',
        ),
        migrations.RemoveField(
            model_name='alumni',
            name='linkedin_link',
        ),
        migrations.RemoveField(
            model_name='alumni',
            name='programme',
        ),
        migrations.AddField(
            model_name='alumni',
            name='year',
            field=models.ForeignKey(to='jobportal.Year', null=True),
        ),
        migrations.AddField(
            model_name='alumni',
            name='year_passing',
            field=models.ForeignKey(related_name='year_passing', to='jobportal.Year', null=True),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='dept',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'year', to='jobportal.Department', chained_field=b'year'),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='prog',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'dept', to='jobportal.Programme', chained_field=b'dept'),
        ),
    ]
