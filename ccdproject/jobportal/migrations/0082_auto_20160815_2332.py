# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-15 18:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0081_userprofile_login_server'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='first_hr_designation',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Designation'),
        ),
        migrations.AlterField(
            model_name='company',
            name='first_hr_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name=b'Email'),
        ),
        migrations.AlterField(
            model_name='company',
            name='first_hr_fax',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name=b'Fax'),
        ),
        migrations.AlterField(
            model_name='company',
            name='first_hr_mobile',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name=b'Mobile'),
        ),
        migrations.AlterField(
            model_name='company',
            name='first_hr_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Full Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='head_hr_designation',
            field=models.CharField(max_length=30, null=True, verbose_name=b'Designation'),
        ),
        migrations.AlterField(
            model_name='company',
            name='head_hr_email',
            field=models.EmailField(max_length=254, null=True, verbose_name=b'Email'),
        ),
        migrations.AlterField(
            model_name='company',
            name='head_hr_fax',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name=b'Fax'),
        ),
        migrations.AlterField(
            model_name='company',
            name='head_hr_mobile',
            field=models.CharField(max_length=12, null=True, verbose_name=b'Contact Number'),
        ),
        migrations.AlterField(
            model_name='company',
            name='head_hr_name',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Full Name'),
        ),
        migrations.AlterField(
            model_name='event',
            name='remark',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name=b'Remark (Optional)'),
        ),
        migrations.AlterField(
            model_name='job',
            name='ctc_btech',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'B.Tech CTC/year'),
        ),
        migrations.AlterField(
            model_name='job',
            name='ctc_ma',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.A. CTC/year'),
        ),
        migrations.AlterField(
            model_name='job',
            name='ctc_msc',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.Sc. CTC/year'),
        ),
        migrations.AlterField(
            model_name='job',
            name='ctc_mtech',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.Tech CTC/year'),
        ),
        migrations.AlterField(
            model_name='job',
            name='ctc_phd',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'Ph.D. CTC/year'),
        ),
        migrations.AlterField(
            model_name='job',
            name='gross_btech',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'B.Tech Gross Salary'),
        ),
        migrations.AlterField(
            model_name='job',
            name='gross_ma',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.A. Gross Salary'),
        ),
        migrations.AlterField(
            model_name='job',
            name='gross_msc',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.Sc. Gross Salary'),
        ),
        migrations.AlterField(
            model_name='job',
            name='gross_mtech',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.Tech Gross Salary'),
        ),
        migrations.AlterField(
            model_name='job',
            name='gross_phd',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'Ph.D. Gross Salary'),
        ),
    ]