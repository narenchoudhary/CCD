# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-28 16:56
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0013_auto_20160927_0323'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='rank_category',
            field=models.CharField(choices=[(b'CML', b'CML'), (b'Non-CML SC', b'Non-CML SC'), (b'Non-CML ST', b'Non-CML ST'), (b'Non-CML OBC', b'Non-CML OBC'), (b'Non-CML NT', b'Non-CML PD'), (b'MA Exam Marks', b'MA Exam Marks')], default=b'CML', help_text=b'Select from Non-CML if your rank is not in CML.', max_length=30, null=True, verbose_name=b'Rank Category'),
        ),
        migrations.AlterField(
            model_name='student',
            name='jee_air_rank',
            field=models.DecimalField(decimal_places=0, default=0, help_text=b'Fill Common Merit List (CML) Rank in the entrance examination.', max_digits=6, null=True, validators=[django.core.validators.MaxValueValidator(40000), django.core.validators.MinValueValidator(1)], verbose_name=b'JEE/GATE/JAM/Other Entrance Exam All India Rank '),
        ),
        migrations.AlterField(
            model_name='student',
            name='percentage_xii',
            field=models.DecimalField(decimal_places=2, default=40, help_text=b'Do not multiply CGPA with any factor. Fill it as it is.', max_digits=5, null=True, verbose_name=b'Class XII Percentage/Diploma (out of 100) OR CGPA (out of 10)'),
        ),
    ]
