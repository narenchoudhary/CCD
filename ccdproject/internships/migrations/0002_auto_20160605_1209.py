# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0001_initial'),
        ('internships', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinternrelation',
            name='stud',
            field=models.ForeignKey(to='jobportal.Student'),
        ),
        migrations.AddField(
            model_name='programmeinternrelation',
            name='dept',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'year', to='jobportal.Department', chained_field=b'year', null=True),
        ),
        migrations.AddField(
            model_name='programmeinternrelation',
            name='intern',
            field=models.ForeignKey(to='internships.IndInternship'),
        ),
        migrations.AddField(
            model_name='programmeinternrelation',
            name='prog',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'dept', to='jobportal.Programme', chained_field=b'dept', null=True),
        ),
        migrations.AddField(
            model_name='programmeinternrelation',
            name='year',
            field=models.ForeignKey(to='jobportal.Year', null=True),
        ),
        migrations.AddField(
            model_name='indinternship',
            name='company_owner',
            field=models.ForeignKey(to='jobportal.Company'),
        ),
    ]
