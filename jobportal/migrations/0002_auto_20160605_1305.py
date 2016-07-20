# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jobportal.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cv',
            name='cv2',
            field=models.FileField(null=True, upload_to=jobportal.models.get_cv2_name, blank=True),
        ),
    ]
