# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-10 04:02
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jobportal.models
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[(b'student', b'student'), (b'alumni', b'alumni'), (b'admin', b'admin'), (b'company', b'company'), (b'verifier', b'verifier')], default=b'admin', max_length=20)),
                ('login_server', models.CharField(blank=True, default=b'dikrong', max_length=30, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_username', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Admin Username')),
                ('position', models.CharField(blank=True, max_length=60, null=True, verbose_name=b'Position')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Alumni',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iitg_webmail', models.CharField(blank=True, max_length=50, verbose_name=b'IITG Webmail')),
                ('alternate_email', models.EmailField(blank=True, max_length=254, verbose_name=b'Alternate Email')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', versatileimagefield.fields.VersatileImageField(null=True, upload_to=jobportal.models.get_avatar_name)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50, null=True, verbose_name=b'Company Name')),
                ('description', models.TextField(null=True, verbose_name=b'Description')),
                ('postal_address', models.TextField(blank=True, null=True, verbose_name=b'Postal Address')),
                ('website', models.CharField(max_length=100, null=True)),
                ('office_contact_no', models.CharField(blank=True, help_text=b'Company contact number (upto 20 digits)', max_length=20, null=True, verbose_name=b'Office Contact Number')),
                ('organization_type', models.CharField(blank=True, choices=[(b'Private', b'Private'), (b'Government', b'Government'), (b'PSU', b'PSU'), (b'MNC(Indian Origin)', b'MNC(Indian Origin)'), (b'MNC(Foreign Origin)', b'MNC(Foreign Origin)'), (b'NGO', b'NGO'), (b'Other', b'Other')], default=b'PSU', max_length=20, verbose_name=b'Organization Type')),
                ('industry_sector', models.CharField(blank=True, choices=[(b'Core Engg', b'Core Engg'), (b'IT', b'IT'), (b'Analytics', b'Analytics'), (b'Management', b'Management'), (b'Finance', b'Finance'), (b'Education', b'Education'), (b'Consulting', b'Consulting'), (b'R&D', b'R&D'), (b'Oil and Gas', b'Oil and Gas'), (b'Ecommerce', b'Ecommerce'), (b'FMCG', b'FMCG'), (b'Manufacturing', b'Manufacturing'), (b'Telecom', b'Telecom'), (b'Other', b'Other')], default=b'IT', max_length=25, verbose_name=b'Industry Sector')),
                ('head_hr_name', models.CharField(max_length=20, null=True, verbose_name=b'Full Name')),
                ('head_hr_email', models.EmailField(max_length=254, null=True, verbose_name=b'Email')),
                ('head_hr_designation', models.CharField(max_length=30, null=True, verbose_name=b'Designation')),
                ('head_hr_mobile', models.CharField(max_length=12, null=True, verbose_name=b'Contact Number')),
                ('head_hr_fax', models.CharField(blank=True, max_length=15, null=True, verbose_name=b'Fax')),
                ('first_hr_name', models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Full Name')),
                ('first_hr_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name=b'Email')),
                ('first_hr_designation', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Designation')),
                ('first_hr_mobile', models.CharField(blank=True, max_length=12, null=True, verbose_name=b'Mobile')),
                ('first_hr_fax', models.CharField(blank=True, max_length=15, null=True, verbose_name=b'Fax')),
                ('approved', models.NullBooleanField(default=None, verbose_name=b'Approval Status')),
                ('approval_date', models.DateTimeField(blank=True, null=True, verbose_name=b'Approval DateTime')),
                ('signup_datetime', models.DateTimeField(blank=True, null=True, verbose_name=b'SignUp DateTime')),
                ('approver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Admin', verbose_name=b'Profile Approver')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv1', models.FileField(blank=True, null=True, upload_to=jobportal.models.get_cv1_name)),
                ('cv2', models.FileField(blank=True, null=True, upload_to=jobportal.models.get_cv2_name)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True, verbose_name=b'Event Title')),
                ('event_type', models.CharField(choices=[(b'Screening Test', b'Screening Test'), (b'Pre Placement Talk', b'Pre Placement Talk'), (b'Workshop', b'Workshop'), (b'Promotional Event', b'Promotional Event')], help_text=b'Select event type from the dropdown menu.', max_length=30, null=True, verbose_name=b'Event Type')),
                ('duration', models.DecimalField(decimal_places=2, default=1, max_digits=4, verbose_name=b'Estimated Duration (in hours)')),
                ('logistics', models.CharField(blank=True, max_length=400, null=True, verbose_name=b'Logistics')),
                ('remark', models.CharField(blank=True, max_length=400, null=True, verbose_name=b'Remark (Optional)')),
                ('final_date', models.DateField(blank=True, help_text=b'This is the date assigned for  the event by the administrator.', null=True, verbose_name=b'Approved Date')),
                ('is_approved', models.NullBooleanField(default=None, verbose_name=b'Approval Status')),
                ('creation_datetime', models.DateTimeField(editable=False, null=True, verbose_name=b'Creation DateTime')),
                ('company_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Company')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name=b'Job Description')),
                ('designation', models.CharField(blank=True, max_length=90, null=True, verbose_name=b'Job Designation')),
                ('profile_name', models.CharField(max_length=50, null=True, verbose_name=b'Profile Name')),
                ('num_openings', models.DecimalField(decimal_places=0, max_digits=3, null=True, verbose_name=b'Expected number of recruitments from IIT Guwahati')),
                ('backlog_filter', models.BooleanField(default=False, verbose_name=b'Backlog Filtering')),
                ('num_backlogs_allowed', models.IntegerField(default=1, verbose_name=b'Number of backlogs permitted')),
                ('cpi_shortlist', models.BooleanField(default=False, verbose_name=b'CPI-Shortlist')),
                ('minimum_cpi', models.DecimalField(blank=True, decimal_places=2, default=4.0, max_digits=4, verbose_name=b'Minimum CPI (On a scale of 0-10)')),
                ('percentage_x', models.DecimalField(decimal_places=2, default=40.0, max_digits=5, null=True, verbose_name=b'Percentage X')),
                ('percentage_xii', models.DecimalField(decimal_places=2, default=40.0, max_digits=5, null=True, verbose_name=b'Percentage XII')),
                ('currency', models.CharField(default=b'INR', max_length=15, null=True)),
                ('ctc_btech', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'B.Tech/B.Des CTC/year')),
                ('ctc_mtech', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.Tech/M.Des CTC/year')),
                ('ctc_msc', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.Sc. CTC/year')),
                ('ctc_ma', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.A. CTC/year')),
                ('ctc_phd', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'Ph.D. CTC/year')),
                ('gross_btech', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'B.Tech/B.Des Gross Salary')),
                ('gross_mtech', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.Tech/M.Des Gross Salary')),
                ('gross_msc', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.Sc. Gross Salary')),
                ('gross_ma', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'M.A. Gross Salary')),
                ('gross_phd', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True, verbose_name=b'Ph.D. Gross Salary')),
                ('additional_info', models.TextField(blank=True, default=b'', null=True, verbose_name=b'Additional Information About Salary (if any)')),
                ('bond_link', models.FileField(blank=True, null=True, upload_to=jobportal.models.get_bond_link_name, verbose_name=b'Legal Bond Document')),
                ('posted_on', models.DateTimeField(blank=True, null=True, verbose_name=b'Creation Date')),
                ('last_updated', models.DateTimeField(blank=True, null=True, verbose_name=b'Last Updatation Date')),
                ('approved', models.NullBooleanField(default=None, verbose_name=b'Approval Status')),
                ('approved_on', models.DateField(blank=True, null=True, verbose_name=b'Approval Date')),
                ('opening_date', models.DateField(blank=True, null=True, verbose_name=b'Opening Date')),
                ('application_deadline', models.DateField(blank=True, null=True, verbose_name=b'Closing Date')),
                ('company_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Company', verbose_name=b'Company Owner')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(null=True, verbose_name=b'Year')),
                ('dept', models.CharField(choices=[(b'Biosciences and Bioengineering', b'Biosciences and Bioengineering'), (b'Chemistry', b'Chemistry'), (b'Chemical Engineering', b'Chemical Engineering'), (b'Civil Engineering', b'Civil Engineering'), (b'Computer Science and Engineering', b'Computer Science and Engineering'), (b'Design', b'Design'), (b'Electronics and Electrical Engineering', b'Electronics and Electrical Engineering'), (b'ECE', b'Electronics'), (b'Humanities & Social Sciences', b'Humanities & Social Sciences'), (b'Mathematics', b'Mathematics'), (b'Mechanical', b'Mechanical'), (b'Physics', b'Physics')], help_text=b'Eg. Department of Chemistry', max_length=80, null=True, verbose_name=b'Department')),
                ('discipline', models.CharField(blank=True, max_length=80, null=True, verbose_name=b'Discipline')),
                ('name', models.CharField(choices=[(b'BTECH', b'B.Tech.'), (b'BDES', b'B.Des.'), (b'MTECH', b'M.Tech.'), (b'MDES', b'M.Des.'), (b'PHD', b'Ph.D.'), (b'MSC', b'M.Sc.'), (b'MA', b'M.A.')], max_length=10, verbose_name=b'Programme Name')),
                ('minor_status', models.BooleanField(default=False, verbose_name=b'Minor Status')),
                ('open_for_placement', models.BooleanField(default=False, verbose_name=b'Open for Placement')),
                ('open_for_internship', models.BooleanField(default=False, verbose_name=b'Open for Internship')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProgrammeJobRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportal.Job')),
                ('prog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Programme')),
            ],
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', versatileimagefield.fields.VersatileImageField(null=True, upload_to=jobportal.models.get_sign_name)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SiteManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_id', models.DecimalField(decimal_places=0, default=0.0, max_digits=1, validators=[django.core.validators.MaxValueValidator(1.0), django.core.validators.MinValueValidator(1.0)])),
                ('job_student_profile_update_deadline', models.DateField(blank=True, null=True)),
                ('job_student_cv_update_deadline', models.DateField(blank=True, null=True)),
                ('job_student_avatar_update_deadline', models.DateField(blank=True, null=True)),
                ('job_student_sign_update_deadline', models.DateField(blank=True, null=True)),
                ('intern_student_profile_update_deadline', models.DateField(blank=True, null=True)),
                ('intern_student_cv_update_deadline', models.DateField(blank=True, null=True)),
                ('intern_student_avatar_update', models.DateField(blank=True, null=True)),
                ('intern_student_sign_update', models.DateField(blank=True, null=True)),
                ('creation_datetime', models.DateTimeField(blank=True, null=True)),
                ('last_update_datetime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iitg_webmail', models.CharField(max_length=50, unique=True, verbose_name=b'IITG Webmail')),
                ('roll_no', models.DecimalField(decimal_places=0, default=0, max_digits=15, unique=True, verbose_name=b'Roll No')),
                ('name', models.CharField(default=b'', max_length=80, verbose_name=b'Full Name')),
                ('dob', models.DateField(blank=True, default=django.utils.timezone.now, verbose_name=b'DOB')),
                ('sex', models.CharField(choices=[(b'M', b'Male'), (b'F', b'Female')], default=b'M', max_length=1, verbose_name=b'Gender')),
                ('active_backlogs', models.IntegerField(default=0, verbose_name=b'Number of active backlogs')),
                ('category', models.CharField(choices=[(b'GEN', b'GEN'), (b'OBC', b'OBC'), (b'SC', b'SC'), (b'ST', b'ST'), (b'PD', b'PD'), (b'FOREIGN', b'FOREIGN')], default=b'GEN', max_length=10)),
                ('nationality', models.CharField(blank=True, default=b'INDIAN', max_length=15)),
                ('minor_year', models.IntegerField(blank=True, null=True, verbose_name=b'Minor Year')),
                ('minor_dept', models.CharField(blank=True, choices=[(b'Biosciences and Bioengineering', b'Biosciences and Bioengineering'), (b'Chemistry', b'Chemistry'), (b'Chemical Engineering', b'Chemical Engineering'), (b'Civil Engineering', b'Civil Engineering'), (b'Computer Science and Engineering', b'Computer Science and Engineering'), (b'Design', b'Design'), (b'Electronics and Electrical Engineering', b'Electronics and Electrical Engineering'), (b'ECE', b'Electronics'), (b'Humanities & Social Sciences', b'Humanities & Social Sciences'), (b'Mathematics', b'Mathematics'), (b'Mechanical', b'Mechanical'), (b'Physics', b'Physics')], help_text=b'Eg. Department of Chemistry', max_length=80, null=True, verbose_name=b'Minor Department')),
                ('minor_discipline', models.CharField(blank=True, max_length=80, null=True, verbose_name=b'Minor Discipline')),
                ('minor_prog', models.CharField(blank=True, choices=[(b'BTECH', b'B.Tech.'), (b'BDES', b'B.Des.'), (b'MTECH', b'M.Tech.'), (b'MDES', b'M.Des.'), (b'PHD', b'Ph.D.'), (b'MSC', b'M.Sc.'), (b'MA', b'M.A.')], max_length=10, null=True)),
                ('year', models.IntegerField(null=True, verbose_name=b'Year')),
                ('dept', models.CharField(choices=[(b'Biosciences and Bioengineering', b'Biosciences and Bioengineering'), (b'Chemistry', b'Chemistry'), (b'Chemical Engineering', b'Chemical Engineering'), (b'Civil Engineering', b'Civil Engineering'), (b'Computer Science and Engineering', b'Computer Science and Engineering'), (b'Design', b'Design'), (b'Electronics and Electrical Engineering', b'Electronics and Electrical Engineering'), (b'ECE', b'Electronics'), (b'Humanities & Social Sciences', b'Humanities & Social Sciences'), (b'Mathematics', b'Mathematics'), (b'Mechanical', b'Mechanical'), (b'Physics', b'Physics')], help_text=b'Eg. Department of Chemistry', max_length=80, null=True, verbose_name=b'Department')),
                ('discipline', models.CharField(max_length=80, null=True, verbose_name=b'Discipline')),
                ('prog', models.CharField(choices=[(b'BTECH', b'B.Tech.'), (b'BDES', b'B.Des.'), (b'MTECH', b'M.Tech.'), (b'MDES', b'M.Des.'), (b'PHD', b'Ph.D.'), (b'MSC', b'M.Sc.'), (b'MA', b'M.A.')], max_length=10, null=True)),
                ('hostel', models.CharField(blank=True, choices=[(b'Barak', b'Barak'), (b'Brahmaputra', b'Brahmaputra'), (b'Dhansiri', b'Dhansiri'), (b'Dibang', b'Dibang'), (b'Dihing', b'Dihing'), (b'Kameng', b'Kameng'), (b'Kapili', b'Kapili'), (b'Lohit', b'Lohit'), (b'Manas', b'Manas'), (b'Married Scholars ', b'Married Scholars'), (b'Siang', b'Siang'), (b'Subansiri', b'Subansiri'), (b'Umiam', b'Umiam'), (b'Other', b'Other')], default=b'', max_length=25)),
                ('room_no', models.CharField(blank=True, default=b'', max_length=6, verbose_name=b'Room No')),
                ('alternative_email', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Alternative Email')),
                ('mobile_campus', models.CharField(blank=True, max_length=16, verbose_name=b'Mobile (Guwahati)')),
                ('mobile_campus_alternative', models.CharField(blank=True, max_length=16, verbose_name=b'Alternative Mobile (Guwahati)')),
                ('mobile_home', models.CharField(blank=True, max_length=16, verbose_name=b'Mobile (Home)')),
                ('address_line1', models.CharField(blank=True, default=b'', max_length=50, verbose_name=b'Permanent Address Line1')),
                ('address_line2', models.CharField(blank=True, default=b'', max_length=50, verbose_name=b'Permanent Address Line2')),
                ('address_line3', models.CharField(blank=True, default=b'', max_length=50, verbose_name=b'Permanent Address Line3')),
                ('pin_code', models.DecimalField(decimal_places=0, default=781039, max_digits=10, verbose_name=b'PIN Code')),
                ('percentage_x', models.DecimalField(blank=True, decimal_places=2, default=40, max_digits=5, verbose_name=b'Percentage X')),
                ('percentage_xii', models.DecimalField(blank=True, decimal_places=2, default=40, max_digits=5, verbose_name=b'Percentage XII')),
                ('board_x', models.CharField(blank=True, default=b'CBSE', max_length=30, null=True, verbose_name=b'X Examination Board')),
                ('board_xii', models.CharField(blank=True, default=b'CBSE', max_length=30, null=True, verbose_name=b'XII Examination Board')),
                ('medium_x', models.CharField(blank=True, default=b'English', max_length=30, null=True, verbose_name=b'X Examination Medium')),
                ('medium_xii', models.CharField(blank=True, default=b'English', max_length=30, null=True, verbose_name=b'XII Examination Medium')),
                ('passing_year_x', models.DecimalField(blank=True, decimal_places=0, default=2003, max_digits=4, verbose_name=b'X Examination Passing Year')),
                ('passing_year_xii', models.DecimalField(blank=True, decimal_places=0, default=2003, max_digits=4, verbose_name=b'XII Examination Passing Year')),
                ('gap_in_study', models.BooleanField(default=False, verbose_name=b'Gap In Study')),
                ('gap_reason', models.TextField(blank=True, default=b'', max_length=100, null=True, verbose_name=b'Reason For Gap In Study')),
                ('jee_air_rank', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=6, null=True, verbose_name=b'JEE AIR Rank')),
                ('linkedin_link', models.URLField(blank=True, max_length=254, null=True, verbose_name=b'LinkedIn Account Public URL')),
                ('cpi', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(0.0)], verbose_name=b'CPI')),
                ('spi_1_sem', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(0.0)], verbose_name=b'SPI 1st Semester')),
                ('spi_2_sem', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(0.0)], verbose_name=b'SPI 2nd Semester')),
                ('spi_3_sem', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(0.0)], verbose_name=b'SPI 3rd Semester')),
                ('spi_4_sem', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(0.0)], verbose_name=b'SPI 4th Semester')),
                ('spi_5_sem', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(0.0)], verbose_name=b'SPI 5th Semester')),
                ('spi_6_sem', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(0.0)], verbose_name=b'SPI 6th Semester')),
                ('fee_transaction_id', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Fee Transaction ID')),
                ('placed', models.BooleanField(default=False, verbose_name=b'Placement Status')),
                ('intern2', models.BooleanField(default=False, verbose_name=b'Second Year Internship Status')),
                ('intern3', models.BooleanField(default=False, verbose_name=b'Third Year Internship Status')),
                ('ppo', models.BooleanField(default=False, verbose_name=b'PPO Status')),
                ('job_candidate', models.BooleanField(default=False)),
                ('intern_candidate', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StudentJobRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortlist_init', models.BooleanField(default=False)),
                ('shortlist_init_datetime', models.DateTimeField(blank=True, null=True)),
                ('placed_init', models.BooleanField(default=False)),
                ('placed_init_datetime', models.DateTimeField(blank=True, null=True)),
                ('placed_approved', models.NullBooleanField(default=None)),
                ('placed_approved_datetime', models.DateTimeField(blank=True, null=True)),
                ('cv1', models.BooleanField(default=False)),
                ('cv2', models.BooleanField(default=False)),
                ('creation_datetime', models.DateTimeField(null=True)),
                ('job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Job')),
                ('stud', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Student')),
            ],
        ),
        migrations.AddField(
            model_name='signature',
            name='stud',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='programme',
            unique_together=set([('year', 'dept', 'discipline', 'name', 'minor_status')]),
        ),
        migrations.AddField(
            model_name='cv',
            name='stud',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Student'),
        ),
        migrations.AddField(
            model_name='avatar',
            name='stud',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.Student'),
        ),
    ]
