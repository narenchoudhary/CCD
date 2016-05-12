# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jobportal.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0036_auto_20160507_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumni',
            name='cv',
            field=models.FileField(null=True, upload_to=jobportal.models.generate_alum_cvname, blank=True),
        ),
    ]
