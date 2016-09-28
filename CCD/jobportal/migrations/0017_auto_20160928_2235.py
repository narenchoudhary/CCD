# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-28 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0016_auto_20160928_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='rank_category',
            field=models.CharField(choices=[(b'CML', b'CML'), (b'Non-CML SC', b'Non-CML SC'), (b'Non-CML ST', b'Non-CML ST'), (b'Non-CML OBC', b'Non-CML OBC'), (b'Non-CML NT', b'Non-CML PD'), (b'MA Exam Marks', b'MA Exam Marks')], default=b'CML', help_text=b'If your rank was not in CML, then select from Non-CML categories.', max_length=30, null=True, verbose_name=b'Rank Category'),
        ),
    ]
