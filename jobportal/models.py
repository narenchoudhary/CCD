from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser

from smart_selects.db_fields import ChainedForeignKey
from versatileimagefield.fields import VersatileImageField

from constants import *


def generate_alum_cvname(instance, filename):
    url = "alum_cv/%s" % str(instance.id)
    return url


def get_cv1_name(instance, filename):
    url = "cv1/%s" % str(instance.stud.id)
    return url


def get_cv2_name(instance, filename):
    url = "cv2/%s" % str(instance.stud.id)
    return url


def get_avatar_name(instance, filename):
    url = "avatar/%s" % str(instance.stud.roll_no)
    return url


def get_sign_name(instance, filename):
    url = "signature/%s" % str(instance.stud.roll_no)
    return url


class UserProfile(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='admin')

    def __unicode__(self):
        return str(self.username)


class Year(models.Model):
    current_year = models.DecimalField(max_digits=4, decimal_places=0, null=True, unique=True)
    remark = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return str(self.current_year)


class Department(models.Model):
    year = models.ForeignKey(Year)
    dept = models.CharField(max_length=40)
    dept_code = models.CharField(max_length=4)

    class Meta:
        unique_together = ['dept_code', 'year']

    def __unicode__(self):
        return str(self.dept_code)


class Programme(models.Model):
    year = models.ForeignKey(Year)
    dept = ChainedForeignKey(Department, chained_field="year", chained_model_field="year", show_all=False)
    name = models.CharField(choices=PROGRAMMES, max_length=10)
    minor_status = models.BooleanField(default=False)

    class Meta:
        unique_together = ['year', 'dept', 'name']

    def __unicode__(self):
        return str(self.name)


class Company(models.Model):
    user = models.OneToOneField(UserProfile, blank=True, null=True)
    company_name = models.CharField(blank=True, null=True, max_length=30, verbose_name="Company")
    description = models.TextField(blank=True, null=True, verbose_name="Brief Writeup on organization")
    postal_address = models.TextField(blank=True, null=True, verbose_name="Postal Address")
    website = models.CharField(default="www.example.com", max_length=100)
    organization_type = models.CharField(max_length=20, choices=ORGANIZATION_TYPE, blank=True,
                                         verbose_name="Type of Organization", default="PSU")
    industry_sector = models.CharField(max_length=25, choices=INDUSTRY_SECTOR, blank=True,
                                       verbose_name="Industry Sector", default="IT")
    # Head Contact
    head_hr_name = models.CharField(max_length=20, default='Mr. Head HR', blank=True)
    head_hr_email = models.CharField(max_length=60, default='headhr@xyz.com', blank=True)
    head_hr_designation = models.CharField(max_length=30, default='Head HR', blank=True)
    head_hr_mobile = models.CharField(max_length=12, default='0123456789', blank=True)
    head_hr_fax = models.CharField(max_length=15, default='0123456', blank=True)
    # First HR
    first_hr_name = models.CharField(max_length=20, default='Mr. First HR', blank=True)
    first_hr_email = models.CharField(max_length=60, default='firsthr@xyz.com', blank=True)
    first_hr_designation = models.CharField(max_length=30, default='First HR', blank=True)
    first_hr_mobile = models.CharField(max_length=12, default='0123456789', blank=True)
    first_hr_fax = models.CharField(max_length=15, default='0123456', blank=True)
    # status
    approved = models.BooleanField(default=False)
    signup_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return str(self.company_name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.signup_date = timezone.now()
        return super(Company, self).save(*args, **kwargs)


class Admin(models.Model):
    user = models.OneToOneField(UserProfile, blank=True, null=True)
    admin_username = models.CharField(max_length=50, null=True, blank=True, verbose_name="Admin Name")
    position = models.CharField(max_length=60, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name_plural = "Admins"

    def __unicode__(self):
        return str(self.id)


class Alumni(models.Model):
    user = models.OneToOneField(UserProfile, blank=True, null=True)
    iitg_webmail = models.CharField(max_length=50, blank=True, verbose_name="IITG Webmail")
    alternate_email = models.EmailField(max_length=254, blank=True, verbose_name="Alternate Email")
    # Foreign Keys
    year = models.ForeignKey(Year, null=True)
    dept = ChainedForeignKey(Department, chained_field='year', chained_model_field='year', show_all=False)
    prog = ChainedForeignKey(Programme, chained_field='dept', chained_model_field='dept', show_all=False)
    year_passing = models.ForeignKey(Year, null=True, related_name='year_passing')

    cv = models.FileField(null=True, upload_to=generate_alum_cvname, blank=True)

    class Meta:
        managed = True

    def __unicode__(self):
        return str(self.user.username)


class Student(models.Model):
    user = models.OneToOneField(UserProfile, blank=True, null=True)
    roll_no = models.DecimalField(max_digits=10, decimal_places=0, unique=True, verbose_name="Roll No", default=0)
    first_name = models.CharField(max_length=20, blank=True, default="")
    middle_name = models.CharField(max_length=20, blank=True, default="")
    last_name = models.CharField(max_length=20, blank=True, default="")
    dob = models.DateField(default=timezone.now, blank=True)
    sex = models.CharField(max_length=1, choices=SEX, default='M')
    category = models.CharField(max_length=10, choices=CATEGORY, default='GEN')
    nationality = models.CharField(max_length=15, default="INDIAN", blank=True)
    minor_programme = models.ForeignKey(Department, null=True, related_name="minor", blank=True)
    jee_air_rank = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    year = models.ForeignKey(Year, null=True)
    dept = ChainedForeignKey(Department, chained_field='year', chained_model_field='year', show_all=False)
    prog = ChainedForeignKey(Programme, chained_field='dept', chained_model_field='dept', show_all=False)
    # campus information
    hostel = models.CharField(max_length=25, choices=HOSTELS, blank=True, default="")
    room_no = models.CharField(max_length=6, blank=True, default="")
    iitg_webmail = models.CharField(max_length=50, blank=False, verbose_name="IITG Webmail", unique=True, default="")
    alternative_email = models.CharField(max_length=50, blank=True, verbose_name="Alternative Email", null=True)
    mobile_campus = models.CharField(blank=True, max_length=16)
    mobile_campus_alternative = models.CharField(blank=True, max_length=16)
    mobile_home = models.CharField(blank=True, max_length=16)
    # permanent address
    address_line1 = models.CharField(default="", max_length=50, blank=True)
    address_line2 = models.CharField(default="", max_length=50, blank=True)
    address_line3 = models.CharField(default="", max_length=50, blank=True)
    pin_code = models.DecimalField(max_digits=10, decimal_places=0, default=781039)
    # board exams
    percentage_x = models.DecimalField(blank=True, max_digits=5, decimal_places=2, null=True)
    percentage_xii = models.DecimalField(blank=True, max_digits=5, decimal_places=2, null=True)
    board_x = models.CharField(max_length=30, blank=True, default="CBSE", null=True)
    board_xii = models.CharField(max_length=30, blank=True, default="CBSE", null=True)
    medium_x = models.CharField(max_length=30, blank=True, null=True, default="English")
    medium_xii = models.CharField(max_length=30, blank=True, null=True, default="English")
    passing_year_x = models.DecimalField(max_digits=4, decimal_places=0, default=2003, blank=True)
    passing_year_xii = models.DecimalField(max_digits=4, decimal_places=0, default=2003, blank=True)
    gap_in_study = models.BooleanField(default=False, blank=True)
    gap_reason = models.TextField(max_length=100, default="", blank=True, null=True)
    linkedin_link = models.URLField(max_length=254, blank=True, null=True)
    # cv fields
    # cv1 = models.FileField(null=True, upload_to=generate_cv1filename, blank=True)
    # cv2 = models.FileField(null=True, upload_to=generate_cv2filename, blank=True)
    # status variables
    placed = models.BooleanField(default=False, blank=True)
    intern2 = models.BooleanField(default=False, blank=True)
    intern3 = models.BooleanField(default=False, blank=True)
    company_count = models.DecimalField(max_digits=30, decimal_places=0, default=0, blank=True, null=True)
    ppo = models.BooleanField(default=False, verbose_name="PPO", blank=True)
    # grades
    cpi = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0.00)
    spi_1_sem = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0.00)
    spi_2_sem = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0.00)
    spi_3_sem = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0.00)
    spi_4_sem = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0.00)
    spi_5_sem = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0.00)
    spi_6_sem = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0.00)
    # jobs
    # jobs = models.ManyToManyField(Job, blank=True, through="StudentJobRelation")

    class Meta:
        managed = True
        verbose_name_plural = "Students"

    def __unicode__(self):
        return str(self.user.username)


class Job(models.Model):
    # Posted by who
    alum_owner = models.ForeignKey(Alumni, blank=True, null=True, related_name="owner")
    company_owner = models.ForeignKey(Company, blank=True, null=True)
    posted_by_alumnus = models.NullBooleanField(default=False, verbose_name="Posted by Alum")
    posted_by_company = models.NullBooleanField(default=False, verbose_name="Posted by Company")
    # Fields Needed
    description = models.TextField(blank=True, verbose_name="Job Description", null=True)
    designation = models.CharField(blank=True, max_length=50, null=True, verbose_name="Job Title/Designation")
    cpi_shortlist = models.BooleanField(default=False)
    minimum_cpi = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=4.00)
    percentage_x = models.DecimalField(max_digits=5, decimal_places=2, default=70.00, null=True)
    percentage_xii = models.DecimalField(max_digits=5, decimal_places=2, default=70.00, null=True)
    num_openings = models.DecimalField(max_digits=3, decimal_places=0, null=True, default=10)
    other_requirements = models.TextField(default="", max_length=100, null=True)
    # Salary
    currency = models.CharField(default="INR", max_length=15, null=True)
    ctc_btech = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    ctc_mtech = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    ctc_msc = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    ctc_ma = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    ctc_phd = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    gross_btech = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    gross_mtech = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    gross_msc = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    gross_ma = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    gross_phd = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    take_home_during_training = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    take_home_after_training = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Bonus/Perks/Incentives",
                                null=True)
    # Job description
    bond = models.NullBooleanField(default=None)
    bond_details = models.TextField(blank=True, null=True, max_length=200)
    bond_link = models.URLField(null=True, blank=True)
    profile_name = models.CharField(max_length=15, null=True)
    # Dates and Status
    posted_on = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    approved = models.NullBooleanField(default=None)
    approved_on = models.DateField(blank=True, null=True)
    opening_date = models.DateField(blank=True, null=True)
    application_deadline = models.DateField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        verbose_name_plural = "Jobs"

    def __unicode__(self):
        return str(self.designation)

    def save(self, *args, **kwargs):
        if not self.id:
            self.posted_on = timezone.now()
            self.opening_date = timezone.now() + timedelta(days=30)
            self.application_deadline = timezone.now() + timedelta(days=45)
        self.last_updated = timezone.now()
        return super(Job, self).save(*args, **kwargs)


class ProgrammeJobRelation(models.Model):
    job = models.ForeignKey(Job)
    year = models.ForeignKey(Year, null=True)
    dept = ChainedForeignKey(Department, chained_field='year', chained_model_field='year', show_all=False, null=True)
    prog = ChainedForeignKey(Programme, chained_field='dept', chained_model_field='dept', show_all=False, null=True)

    def __unicode__(self):
        return str(self.job)


class StudentJobRelation(models.Model):
    # status variables
    round = models.IntegerField(default=1)
    placed_init = models.BooleanField(default=False)
    shortlist_init = models.BooleanField(default=False)
    shortlist_approved = models.NullBooleanField(default=None)
    placed_approved = models.NullBooleanField(default=None)
    dropped = models.BooleanField(default=False)
    # cv
    cv1 = models.BooleanField(default=False)
    cv2 = models.BooleanField(default=False)
    # Foreign Keys
    stud = models.ForeignKey(Student, null=True, blank=True)
    job = models.ForeignKey(Job, null=True, blank=True)

    def __unicode__(self):
        return str(self.id)


# TODO: Replace this with new calendar app
class Event(models.Model):
    alum_owner = models.ForeignKey(Alumni, null=True, blank=True)
    company_owner = models.ForeignKey(Company, null=True, blank=True)
    title = models.CharField(max_length=30, null=True)
    date1 = models.DateField()
    date2 = models.DateField()
    date3 = models.DateField()
    final_date = models.DateField(null=True, blank=True)
    finalised = models.BooleanField(default=False)

    class Meta:
        managed = True
        verbose_name_plural = 'Events'

    def __unicode__(self):
        return str(self.id)


class CompanyReg(models.Model):
    company_name_reg = models.CharField(blank=True, null=True, max_length=30, verbose_name="Company")
    description_reg = models.TextField(blank=True, null=True, verbose_name="Brief Writeup on organization")
    postal_address_reg = models.TextField(blank=True, null=True, verbose_name="Postal Address")
    website_reg = models.CharField(default="www.example.com", max_length=100)
    organization_type_reg = models.CharField(max_length=20, choices=ORGANIZATION_TYPE, blank=True,
                                             verbose_name="Type of Organization", default="PSU")
    industry_sector_reg = models.CharField(max_length=25, choices=INDUSTRY_SECTOR, blank=True,
                                           verbose_name="Industry Sector", default="IT")
    # Head Contact
    head_hr_name_reg = models.CharField(max_length=20, default='Mr. Head HR', blank=True)
    head_hr_email_reg = models.CharField(max_length=60, default='headhr@xyz.com', blank=True)
    head_hr_designation_reg = models.CharField(max_length=30, default='Head HR', blank=True)
    head_hr_mobile_reg = models.CharField(max_length=12, default='0123456789', blank=True)
    head_hr_fax_reg = models.CharField(max_length=15, default='0123456', blank=True)
    # First HR
    first_hr_name_reg = models.CharField(max_length=20, default='Mr. First HR', blank=True)
    first_hr_email_reg = models.CharField(max_length=60, default='firsthr@xyz.com', blank=True)
    first_hr_designation_reg = models.CharField(max_length=30, default='First HR', blank=True)
    first_hr_mobile_reg = models.CharField(max_length=12, default='0123456789', blank=True)
    first_hr_fax_reg = models.CharField(max_length=15, default='0123456', blank=True)

    def __unicode__(self):
        return str(self.company_name_reg)


class Avatar(models.Model):
    stud = models.ForeignKey(Student, blank=True, null=True)
    avatar = models.ImageField(upload_to=get_avatar_name, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            this = Avatar.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except Avatar.DoesNotExist:
            pass
        super(Avatar, self).save(*args, **kwargs)


class Signature(models.Model):
    stud = models.ForeignKey(Student, blank=True, null=True)
    signature = models.ImageField(upload_to=get_sign_name, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            this = Signature.objects.get(id=self.id)
            if this.signature != self.signature:
                this.signature.delete(save=False)
        except Signature.DoesNotExist:
            pass
        super(Signature, self).save(*args, **kwargs)


class CV(models.Model):
    stud = models.ForeignKey(Student, blank=True, null=True)
    cv1 = models.FileField(upload_to=get_cv1_name, blank=True, null=True)
    cv2 = models.FileField(upload_to=get_cv2_name, blank=True, null=True)
