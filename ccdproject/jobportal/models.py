import uuid

from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from smart_selects.db_fields import ChainedForeignKey

from constants import *


def generate_alum_cvname(instance, filename):
    url = "alum_cv/{0}_{1}".format(instance.id, uuid.uuid4())
    return url


def get_cv1_name(instance, filename):
    url = 'studcv/{0}/{0}_cv1_{1}'.format(instance.stud.roll_no, uuid.uuid4())
    return url


def get_cv2_name(instance, filename):
    url = 'studcv/{0}/{0}_cv2_{1}'.format(instance.stud.roll_no, uuid.uuid4())
    return url


def get_avatar_name(instance, filename):
    url = "studavatar/{0}_{1}".format(instance.stud.roll_no, uuid.uuid4())
    return url


def get_sign_name(instance, filename):
    url = "studsignature/{0}_{1}".format(instance.stud.roll_no, uuid.uuid4())
    return url


def get_bond_link_name(instance, filename):
    url = "company_bond/{0}_{1}".format(instance.company.user.username,
                                        uuid.uuid4())
    return url


class UserProfile(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPE,
                                 default='admin')
    login_server = models.CharField(max_length=30, choices=SERVER_IP,
                                    default='202.141.80.13')

    def __unicode__(self):
        return str(self.username)


class Year(models.Model):
    current_year = models.DecimalField(max_digits=4, decimal_places=0,
                                       null=True, unique=True)
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
    year = models.ForeignKey(Year, verbose_name='Year')
    dept = ChainedForeignKey(Department, chained_field="year",
                             chained_model_field="year", show_all=False,
                             verbose_name='Department')
    name = models.CharField(choices=PROGRAMMES, max_length=10,
                            verbose_name='Programme Name')
    minor_status = models.BooleanField(default=False,
                                       verbose_name='Minor Status')
    open_for_placement = models.BooleanField(default=False,
                                             verbose_name='Open for Placement')
    open_for_internship = models.BooleanField(default=False,
                                              verbose_name='Open for Internship')

    class Meta:
        unique_together = ['year', 'dept', 'name', 'minor_status']

    def __unicode__(self):
        return str(self.name)


class Admin(models.Model):
    user = models.OneToOneField(UserProfile, blank=True, null=True,
                                limit_choices_to={'user_type': 'admin'})
    admin_username = models.CharField(max_length=50, null=True, blank=True,
                                      verbose_name="Admin Username")
    position = models.CharField(max_length=60, null=True, blank=True,
                                verbose_name='Position')

    class Meta:
        managed = True

    def __unicode__(self):
        return str(self.user.username)


class Company(models.Model):
    user = models.OneToOneField(UserProfile, blank=True, null=True,
                                limit_choices_to={'user_type': 'company'})
    company_name = models.CharField(blank=False, null=True, max_length=30,
                                    verbose_name="Company Name")
    description = models.TextField(blank=False, null=True,
                                   verbose_name="Description")
    postal_address = models.TextField(blank=True, null=True,
                                      verbose_name="Postal Address")
    website = models.CharField(blank=False, null=True, max_length=100)
    office_contact_no = models.CharField(max_length=20, null=True,
                                         blank=True,
                                         verbose_name='Office Contact Number',
                                         help_text="Company contact number "
                                                   "(upto 20 digits)")
    organization_type = models.CharField(max_length=20,
                                         choices=ORGANIZATION_TYPE, blank=True,
                                         verbose_name="Organization Type",
                                         default="PSU")
    industry_sector = models.CharField(max_length=25, choices=INDUSTRY_SECTOR,
                                       blank=True,  default="IT",
                                       verbose_name="Industry Sector")
    # Head Contact
    head_hr_name = models.CharField(max_length=20, null=True, blank=False,
                                    verbose_name='Full Name')
    head_hr_email = models.EmailField(null=True, blank=False,
                                      verbose_name='Email')
    head_hr_designation = models.CharField(max_length=30, blank=False,
                                           null=True,
                                           verbose_name='Designation')
    head_hr_mobile = models.CharField(max_length=12, blank=False, null=True,
                                      verbose_name='Contact Number')
    head_hr_fax = models.CharField(max_length=15, blank=True, null=True,
                                   verbose_name='Fax')
    # First HR
    first_hr_name = models.CharField(max_length=20, null=True, blank=True,
                                     verbose_name='Full Name')
    first_hr_email = models.EmailField(null=True, blank=True,
                                       verbose_name='Email')
    first_hr_designation = models.CharField(max_length=30, null=True,
                                            blank=True,
                                            verbose_name='Designation'
                                            )
    first_hr_mobile = models.CharField(max_length=12, null=True, blank=True,
                                       verbose_name='Mobile')
    first_hr_fax = models.CharField(max_length=15, null=True, blank=True,
                                    verbose_name='Fax')
    # status
    approver = models.ForeignKey(Admin, null=True,
                                 verbose_name='Profile Approver')
    approved = models.NullBooleanField(default=None,
                                       verbose_name='Approval Status')
    approval_date = models.DateTimeField(null=True, blank=True,
                                         verbose_name='Approval DateTime')
    signup_datetime = models.DateTimeField(null=True, blank=True,
                                           verbose_name='SignUp DateTime')

    def __unicode__(self):
        return str(self.company_name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.signup_datetime = timezone.now()
        return super(Company, self).save(*args, **kwargs)


class Alumni(models.Model):
    user = models.OneToOneField(UserProfile, blank=True, null=True,
                                limit_choices_to={'user_type': 'alumni'})
    iitg_webmail = models.CharField(max_length=50, blank=True,
                                    verbose_name="IITG Webmail")
    alternate_email = models.EmailField(max_length=254, blank=True,
                                        verbose_name="Alternate Email")
    # Foreign Keys
    year = models.ForeignKey(Year, null=True)
    dept = ChainedForeignKey(Department, chained_field='year',
                             chained_model_field='year', show_all=False)
    prog = ChainedForeignKey(Programme, chained_field='dept',
                             chained_model_field='dept', show_all=False)
    year_passing = models.ForeignKey(Year, null=True,
                                     related_name='year_passing')

    cv = models.FileField(null=True, blank=True,
                          upload_to=generate_alum_cvname)

    class Meta:
        managed = True

    def __unicode__(self):
        return str(self.user.username)


class Student(models.Model):
    user = models.OneToOneField(UserProfile, blank=True, null=True,
                                limit_choices_to={'user_type': 'student'})
    iitg_webmail = models.CharField(max_length=50, blank=False,
                                    verbose_name="IITG Webmail",
                                    unique=True)
    roll_no = models.DecimalField(max_digits=10, decimal_places=0, unique=True,
                                  verbose_name="Roll No", default=0)
    name = models.CharField(max_length=60, default="",
                            verbose_name="Full Name")
    dob = models.DateField(default=timezone.now, blank=True,
                           verbose_name='DOB')
    sex = models.CharField(max_length=1, choices=SEX, default='M',
                           verbose_name='Gender')
    active_backlogs = models.IntegerField(verbose_name="Number of active "
                                                       "backlogs", default=0)
    category = models.CharField(max_length=10, choices=CATEGORY, default='GEN')
    nationality = models.CharField(max_length=15, default="INDIAN", blank=True)
    minor_year = models.ForeignKey(Year, null=True, blank=True,
                                   related_name='minor_year',
                                   verbose_name='Minor Programme Year')
    minor_dept = ChainedForeignKey(Department, chained_field='minor_year',
                                   chained_model_field='year',
                                   show_all=False, related_name='minor_dept',
                                   null=True, blank=True,
                                   verbose_name='Minor Programme Department')
    minor_prog = ChainedForeignKey(Programme, chained_field='minor_dept',
                                   chained_model_field='dept',
                                   show_all=False, related_name='minor_prog',
                                   null=True, blank=True,
                                   limit_choices_to={'minor_status': True},
                                   verbose_name='Minor Programme Name')
    year = models.ForeignKey(Year, null=True, blank=True,
                             verbose_name='Major Programme Year')
    dept = ChainedForeignKey(Department, chained_field='year',
                             chained_model_field='year', show_all=False,
                             null=True, blank=True,
                             verbose_name='Major Programme Department')
    prog = ChainedForeignKey(Programme, chained_field='dept',
                             chained_model_field='dept', show_all=False,
                             null=True, blank=True,
                             limit_choices_to={'minor_status': False},
                             verbose_name='Major Programme Name')
    # campus information
    hostel = models.CharField(max_length=25, choices=HOSTELS,
                              blank=True, default="")
    room_no = models.CharField(max_length=6, blank=True, default="",
                               verbose_name='Room No')
    alternative_email = models.CharField(max_length=50, blank=True, null=True,
                                         verbose_name='Alternative Email')
    mobile_campus = models.CharField(blank=True, max_length=16,
                                     verbose_name='Mobile (Guwahati)')
    mobile_campus_alternative = models.CharField(blank=True, max_length=16,
                                                 verbose_name='Alternative Mobile (Guwahati)')
    mobile_home = models.CharField(blank=True, max_length=16,
                                   verbose_name='Mobile (Home)')
    # permanent address
    address_line1 = models.CharField(default="", max_length=50, blank=True,
                                     verbose_name='Permanent Address Line1')
    address_line2 = models.CharField(default="", max_length=50, blank=True,
                                     verbose_name='Permanent Address Line2')
    address_line3 = models.CharField(default="", max_length=50, blank=True,
                                     verbose_name='Permanent Address Line3')
    pin_code = models.DecimalField(max_digits=10, decimal_places=0,
                                   default=781039, verbose_name='PIN Code')
    # board exams
    percentage_x = models.DecimalField(blank=True, max_digits=5,
                                       decimal_places=2, default=40,
                                       verbose_name='Percentage X')
    percentage_xii = models.DecimalField(blank=True, max_digits=5,
                                         decimal_places=2, default=40,
                                         verbose_name='Percentage XII')
    board_x = models.CharField(max_length=30, blank=True, default="CBSE",
                               null=True, verbose_name='X Examination Board')
    board_xii = models.CharField(max_length=30, blank=True, default="CBSE",
                                 null=True,
                                 verbose_name='XII Examination Board')
    medium_x = models.CharField(max_length=30, blank=True, null=True,
                                default="English",
                                verbose_name='X Examination Medium')
    medium_xii = models.CharField(max_length=30, blank=True, null=True,
                                  default="English",
                                  verbose_name='XII Examination Medium')
    passing_year_x = models.DecimalField(max_digits=4, decimal_places=0,
                                         default=2003, blank=True,
                                         verbose_name='X Examination Passing Year')
    passing_year_xii = models.DecimalField(max_digits=4, decimal_places=0,
                                           default=2003, blank=True,
                                           verbose_name='XII Examination Passing Year')
    gap_in_study = models.BooleanField(default=False, blank=True,
                                       verbose_name='Gap In Study')
    gap_reason = models.TextField(max_length=100, default="", blank=True,
                                  null=True,
                                  verbose_name='Reason For Gap In Study')
    jee_air_rank = models.DecimalField(max_digits=6, decimal_places=0,
                                       default=0, verbose_name='JEE AIR Rank')
    linkedin_link = models.URLField(max_length=254, blank=True, null=True,
                                    verbose_name='LinkedIn Account Public URL')
    # grades
    cpi = models.DecimalField(max_digits=4, decimal_places=2, blank=True,
                              default=0.00, verbose_name='CPI',
                              validators=[MaxValueValidator(10.0),
                                          MinValueValidator(0.0)])
    spi_1_sem = models.DecimalField(max_digits=4, decimal_places=2, blank=True,
                                    default=0.00,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(0.0)],
                                    verbose_name='SPI 1st Semester')
    spi_2_sem = models.DecimalField(max_digits=4, decimal_places=2, blank=True,
                                    default=0.00,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(0.0)],
                                    verbose_name='SPI 2nd Semester')
    spi_3_sem = models.DecimalField(max_digits=4, decimal_places=2, blank=True,
                                    default=0.00,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(0.0)],
                                    verbose_name='SPI 3rd Semester')
    spi_4_sem = models.DecimalField(max_digits=4, decimal_places=2, blank=True,
                                    default=0.00,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(0.0)],
                                    verbose_name='SPI 4th Semester')
    spi_5_sem = models.DecimalField(max_digits=4, decimal_places=2, blank=True,
                                    default=0.00,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(0.0)],
                                    verbose_name='SPI 5th Semester')
    spi_6_sem = models.DecimalField(max_digits=4, decimal_places=2, blank=True,
                                    default=0.00,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(0.0)],
                                    verbose_name='SPI 6th Semester')
    # fee details
    fee_transaction_id = models.CharField(max_length=100, null=True,
                                          blank=True,
                                          verbose_name="Fee Transaction ID")
    # status
    placed = models.BooleanField(default=False, blank=True,
                                 verbose_name='Placement Status')
    intern2 = models.BooleanField(default=False, blank=True,
                                  verbose_name='Second Year Internship Status')
    intern3 = models.BooleanField(default=False, blank=True,
                                  verbose_name='Third Year Internship Status')
    ppo = models.BooleanField(default=False, blank=True,
                              verbose_name='PPO Status')

    class Meta:
        managed = True

    def __unicode__(self):
        return str(self.roll_no)


class Job(models.Model):
    company_owner = models.ForeignKey(Company, blank=True, null=True,
                                      verbose_name='Company Owner')
    # Fields Needed
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Job Description')
    designation = models.CharField(blank=True, max_length=50, null=True,
                                   verbose_name='Job Designation')
    profile_name = models.CharField(max_length=50, null=True,
                                    verbose_name='Profile Name')
    num_openings = models.DecimalField(max_digits=3, decimal_places=0,
                                       null=True, blank=True, default=10,
                                       verbose_name='Expected number of '
                                                    'recruitments from IIT '
                                                    'Guwahati')
    # requirements
    backlog_filter = models.BooleanField(default=False,
                                         verbose_name="Backlog Filtering")
    num_backlogs_allowed = models.IntegerField(
        default=1, verbose_name="Number of backlogs permitted")
    cpi_shortlist = models.BooleanField(default=False,
                                        verbose_name='CPI-Shortlist')
    minimum_cpi = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, default=4.00,
        verbose_name='Minimum CPI (On a scale of 0-10)')
    percentage_x = models.DecimalField(max_digits=5, decimal_places=2,
                                       default=40.00, null=True,
                                       verbose_name='Percentage X')
    percentage_xii = models.DecimalField(max_digits=5, decimal_places=2,
                                         default=40.00, null=True,
                                         verbose_name='Percentage XII')
    # Salary
    currency = models.CharField(default="INR", max_length=15, null=True)
    ctc_btech = models.DecimalField(max_digits=16, decimal_places=2,
                                    default=0.00, null=True,
                                    blank=True, verbose_name='B.Tech CTC/year')
    ctc_mtech = models.DecimalField(max_digits=16, decimal_places=2,
                                    default=0.00, null=True,
                                    blank=True, verbose_name='M.Tech CTC/year')
    ctc_msc = models.DecimalField(max_digits=16, decimal_places=2,
                                  default=0.00, null=True,
                                  blank=True, verbose_name='M.Sc. CTC/year')
    ctc_ma = models.DecimalField(max_digits=16, decimal_places=2,
                                 default=0.00, null=True,
                                 blank=True, verbose_name='M.A. CTC/year')
    ctc_phd = models.DecimalField(max_digits=16, decimal_places=2,
                                  default=0.00, null=True,
                                  blank=True, verbose_name='Ph.D. CTC/year')
    gross_btech = models.DecimalField(max_digits=16, decimal_places=2,
                                      default=0.00, null=True,
                                      blank=True,
                                      verbose_name='B.Tech Gross Salary')
    gross_mtech = models.DecimalField(max_digits=16, decimal_places=2,
                                      default=0.00, null=True,
                                      blank=True,
                                      verbose_name='M.Tech Gross Salary')
    gross_msc = models.DecimalField(max_digits=16, decimal_places=2,
                                    default=0.00, null=True,
                                    blank=True,
                                    verbose_name='M.Sc. Gross Salary')
    gross_ma = models.DecimalField(max_digits=16, decimal_places=2,
                                   default=0.00, null=True,
                                   blank=True,
                                   verbose_name='M.A. Gross Salary')
    gross_phd = models.DecimalField(max_digits=16, decimal_places=2,
                                    default=0.00, null=True,
                                    blank=True,
                                    verbose_name='Ph.D. Gross Salary')
    # Job description
    # bond = models.BooleanField(default=False, verbose_name='Legal Bond')
    bond_link = models.FileField(null=True, blank=True,
                                 verbose_name='Legal Bond Document')
    # Dates and Status
    posted_on = models.DateTimeField(blank=True, null=True,
                                     verbose_name='Creation Date')
    last_updated = models.DateTimeField(null=True, blank=True,
                                        verbose_name='Last Updatation Date')
    approved = models.NullBooleanField(default=None,
                                       verbose_name='Approval Status')
    approved_on = models.DateField(blank=True, null=True,
                                   verbose_name='Approval Date')
    opening_date = models.DateField(blank=True, null=True,
                                    verbose_name='Opening Date')
    application_deadline = models.DateField(blank=True, null=True,
                                            verbose_name='Closing Date')

    class Meta:
        managed = True

    def __unicode__(self):
        return str(self.designation)

    def save(self, *args, **kwargs):
        if not self.id:
            self.posted_on = timezone.now()
            self.opening_date = timezone.now() + timedelta(days=30)
            self.application_deadline = timezone.now() + timedelta(days=45)
        self.last_updated = timezone.now()
        if self.minimum_cpi is None:
            self.minimum_cpi = 4.0
        return super(Job, self).save(*args, **kwargs)


class StudentJobRelation(models.Model):
    shortlist_init = models.BooleanField(default=False)
    shortlist_init_datetime = models.DateTimeField(null=True, blank=True)
    # shortlist_approved = models.NullBooleanField(default=None)
    # shortlist_approved_date = models.DateTimeField(null=True, blank=True)
    placed_init = models.BooleanField(default=False)
    placed_init_datetime = models.DateTimeField(null=True, blank=True)
    placed_approved = models.NullBooleanField(default=None)
    placed_approved_datetime = models.DateTimeField(null=True, blank=True)
    # dropped = models.BooleanField(default=False)
    # dropped_date = models.DateTimeField(null=True, blank=True)

    cv1 = models.BooleanField(default=False)
    cv2 = models.BooleanField(default=False)

    stud = models.ForeignKey(Student, null=True, blank=True)
    job = models.ForeignKey(Job, null=True, blank=True)
    creation_datetime = models.DateTimeField(null=True)

    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_datetime = timezone.now()
        return super(StudentJobRelation, self).save(*args, **kwargs)


class Event(models.Model):
    company_owner = models.ForeignKey(Company, null=True, blank=True)
    title = models.CharField(max_length=30, null=True,
                             verbose_name='Event Title')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE,null=True,
                                  verbose_name='Event Type',
                                  help_text='Select event type from the '
                                            'dropdown menu.')
    duration = models.DecimalField(default=1, max_digits=4, decimal_places=2,
                                   verbose_name="Estimated Duration (in "
                                                "hours)")
    logistics = models.CharField(null=True, blank=True, max_length=150,
                                 verbose_name="Logistics")
    remark = models.CharField(max_length=300, null=True, blank=True,
                              verbose_name='Remark (Optional)')
    final_date = models.DateField(null=True, blank=True,
                                  verbose_name='Approved Date',
                                  help_text="This is the date assigned for "
                                            " the event by Administrator.")
    is_approved = models.NullBooleanField(default=None,
                                          verbose_name='Approval Status')
    creation_datetime = models.DateTimeField(editable=False, null=True,
                                             verbose_name='Creation DateTime')

    class Meta:
        managed = True

    def __unicode__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_datetime = timezone.now()
        return super(Event, self).save(*args, **kwargs)


class Avatar(models.Model):
    stud = models.OneToOneField(Student, null=True,
                                on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=get_avatar_name,
                               blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            this = Avatar.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except Avatar.DoesNotExist:
            pass
        super(Avatar, self).save(*args, **kwargs)


class Signature(models.Model):
    stud = models.OneToOneField(Student, on_delete=models.CASCADE,
                                null=True)
    signature = models.ImageField(upload_to=get_sign_name, blank=True,
                                  null=True)

    def save(self, *args, **kwargs):
        try:
            this = Signature.objects.get(id=self.id)
            if this.signature != self.signature:
                this.signature.delete(save=False)
        except Signature.DoesNotExist:
            pass
        super(Signature, self).save(*args, **kwargs)


class CV(models.Model):
    stud = models.OneToOneField(Student, null=True, on_delete=models.CASCADE)
    cv1 = models.FileField(upload_to=get_cv1_name, blank=True, null=True)
    cv2 = models.FileField(upload_to=get_cv2_name, blank=True, null=True)


class ProgrammeJobRelation(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, null=True, on_delete=models.CASCADE)
    dept = ChainedForeignKey(Department, chained_field='year',
                             chained_model_field='year', show_all=False,
                             null=True, on_delete=models.CASCADE)
    prog = ChainedForeignKey(Programme, chained_field='dept',
                             chained_model_field='dept',
                             show_all=False, null=True,
                             on_delete=models.CASCADE)

    def __unicode__(self):
        if self.prog.minor_status:
            return str(self.year) + str(self.dept) + str(self.prog) + '-MINOR'
        else:
            return str(self.year) + str(self.dept) + str(self.prog) + '-MAJOR'
