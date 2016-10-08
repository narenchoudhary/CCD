from datetime import timedelta
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from versatileimagefield.fields import VersatileImageField

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
    url = "studavatar/{0}_{1}.jpg".format(instance.stud.roll_no, uuid.uuid4())
    return url


def get_sign_name(instance, filename):
    url = "studsignature/{0}_{1}".format(instance.stud.roll_no, uuid.uuid4())
    return url


def get_bond_link_name(instance, filename):
    url = "company_bond/{0}_{1}.pdf".format(
        instance.company_owner.user.username, uuid.uuid4())
    return url


class SiteManagement(models.Model):
    site_id = models.DecimalField(
        max_digits=1, decimal_places=0, blank=False, null=False, default=0.00,
        validators=[MaxValueValidator(1.0), MinValueValidator(1.0)],
        unique=True
    )
    job_student_profile_update_deadline = models.DateTimeField(
        null=True, blank=True)
    job_student_cv_update_deadline = models.DateTimeField(null=True,
                                                          blank=True)
    job_student_avatar_update_deadline = models.DateTimeField(
        null=True, blank=True)
    job_student_sign_update_deadline = models.DateTimeField(
        null=True, blank=True)
    job_stud_photo_allowed = models.BooleanField(
        default=False, verbose_name='Allow Avatar Upload for Job Candidates')
    job_stud_sign_allowed = models.BooleanField(
        default=False, verbose_name='Allow Sign Upload for Intern Candidates')
    intern_student_profile_update_deadline = models.DateTimeField(
        null=True, blank=True)
    intern_student_cv_update_deadline = models.DateTimeField(
        null=True, blank=True)
    intern_student_avatar_update_deadline = models.DateTimeField(null=True,
                                                                 blank=True)
    intern_student_sign_update_deadline = models.DateTimeField(null=True,
                                                               blank=True)
    creation_datetime = models.DateTimeField(null=True, blank=True)
    last_update_datetime = models.DateTimeField(null=True, blank=True)
    
    def save(self, **kwargs):
        if not self.id:
            self.creation_datetime = timezone.now()
            self.last_update_datetime = timezone.now()
        else:
            self.last_update_datetime = timezone.now()
        super(SiteManagement, self).save(**kwargs)


class UserProfile(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPE,
                                 default='admin')
    login_server = models.CharField(max_length=30, default='dikrong',
                                    blank=True, null=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __unicode__(self):
        return str(self.username)

    def stud_programme(self):
        stud = Student.objects.filter(user__username=self.username)
        if len(stud) > 0:
            return str(stud[0].prog)
        return ""


class Programme(models.Model):
    year = models.IntegerField(null=True, blank=False, verbose_name='Year')
    year_passing = models.IntegerField(null=True, blank=False, default=2017,
                                       verbose_name='Year of passing', )
    dept = models.CharField(choices=DEPARTMENTS, max_length=80, null=True,
                            blank=False, verbose_name='Department',
                            help_text='Eg. Department of Chemistry')
    discipline = models.CharField(max_length=80, null=True, blank=True,
                                  verbose_name='Discipline')
    name = models.CharField(choices=PROGRAMMES, max_length=10,
                            verbose_name='Programme Name')
    minor_status = models.BooleanField(default=False,
                                       verbose_name='Minor Status')
    open_for_placement = models.BooleanField(default=False,
                                             verbose_name='Open for Placement')
    open_for_internship = models.BooleanField(default=False,
                                              verbose_name=
                                              'Open for Internship')

    class Meta:
        unique_together = ['year', 'dept', 'discipline', 'name',
                           'minor_status']
        managed = True

    def __unicode__(self):
        year = str(self.year)
        dept = str(self.dept)
        discipline = str(self.discipline)
        minor = "Minor" if self.minor_status else "Major"
        return year + " " + dept + " " + discipline + " " + minor


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
    company_name = models.CharField(blank=False, null=True, max_length=50,
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

    class Meta:
        managed = True

    def __unicode__(self):
        return str(self.user.username)


class Student(models.Model):
    user = models.OneToOneField(UserProfile, blank=False, null=False,
                                limit_choices_to={'user_type': 'student'})
    iitg_webmail = models.CharField(max_length=50, blank=False,
                                    verbose_name="IITG Webmail",
                                    unique=True)
    roll_no = models.DecimalField(max_digits=15, decimal_places=0, unique=True,
                                  verbose_name="Roll No", default=0)
    name = models.CharField(max_length=80, default="",
                            verbose_name="Full Name")
    dob = models.DateField(default=timezone.now, blank=False, null=True,
                           verbose_name='DOB')
    sex = models.CharField(max_length=1, choices=SEX, default='M',
                           verbose_name='Gender')
    active_backlogs = models.IntegerField(
        default=0, blank=False, verbose_name="Number of active backlogs")
    category = models.CharField(max_length=40, choices=CATEGORY, default='GEN')
    nationality = models.CharField(max_length=15, default="INDIAN", blank=True)
    minor_year = models.IntegerField(null=True, blank=True,
                                     verbose_name='Minor Year')
    minor_year_passing = models.IntegerField(
        null=True, blank=True, default=2017,
        verbose_name='Minor Year of Passing'
    )
    minor_dept = models.CharField(choices=DEPARTMENTS, max_length=80,
                                  null=True, blank=True,
                                  verbose_name='Minor Department',
                                  help_text='Eg. Department of Chemistry')
    minor_discipline = models.CharField(max_length=80, null=True, blank=True,
                                        verbose_name='Minor Discipline')
    minor_prog = models.CharField(choices=PROGRAMMES, max_length=10,
                                  null=True, blank=True)
    year = models.IntegerField(null=True, blank=False, verbose_name='Year')
    year_passing = models.IntegerField(null=True, blank=True, default=2017,
                                       verbose_name='Year of Passing')
    dept = models.CharField(choices=DEPARTMENTS, max_length=80, null=True,
                            blank=False, verbose_name='Department',
                            help_text='Eg. Department of Chemistry')
    discipline = models.CharField(max_length=80, null=True, blank=False,
                                  verbose_name='Discipline')
    prog = models.CharField(choices=PROGRAMMES, max_length=10, null=True,
                            blank=False)
    # campus information
    hostel = models.CharField(
        max_length=25, choices=HOSTELS, blank=False, default="Manas")
    room_no = models.CharField(
        max_length=6, blank=False, default="B-208", verbose_name='Room No')
    alternative_email = models.CharField(
        max_length=50, blank=False, null=True,
        verbose_name='Alternative Email')
    mobile_campus = models.CharField(
        blank=False, max_length=16, verbose_name='Mobile (Guwahati)')
    mobile_campus_alternative = models.CharField(
        blank=True, max_length=16, verbose_name='Alternative Mobile (Guwahati)'
    )
    mobile_home = models.CharField(
        blank=False, null=True, max_length=16, verbose_name='Mobile (Home)')
    # permanent address
    address_line1 = models.CharField(default="", max_length=50, blank=False,
                                     verbose_name='Permanent Address Line1')
    address_line2 = models.CharField(default="", max_length=50, blank=False,
                                     verbose_name='Permanent Address Line2')
    address_line3 = models.CharField(default="", max_length=50, blank=True,
                                     verbose_name='Permanent Address Line3')
    pin_code = models.DecimalField(max_digits=10, decimal_places=0,
                                   blank=False, null=False, default=781039,
                                   verbose_name='PIN Code')
    # board exams
    percentage_x = models.DecimalField(
        blank=False, null=True, max_digits=5, decimal_places=2, default=40,
        verbose_name='Class X Percentage (out of 100) OR CGPA (out of 10)',
        help_text='Do not multiply CGPA with any factor. Fill it as it is.'
    )
    percentage_xii = models.DecimalField(
        blank=False, null=True, max_digits=5, decimal_places=2, default=40,
        verbose_name='Class XII Percentage/Diploma (out of 100) '
                     'OR CGPA (out of 10)',
        help_text='Do not multiply CGPA with any factor. Fill it as it is.'
    )
    board_x = models.CharField(
        max_length=30, blank=False, default="CBSE", null=True,
        verbose_name='X Examination Board')
    board_xii = models.CharField(
        max_length=30, blank=False, default="CBSE", null=True,
        verbose_name='XII Examination Board')
    medium_x = models.CharField(
        max_length=30, blank=False, null=True, default="English",
        verbose_name='X Examination Medium')
    medium_xii = models.CharField(
        max_length=30, blank=False, null=True, default="English",
        verbose_name='XII Examination Medium')
    passing_year_x = models.DecimalField(
        max_digits=4, decimal_places=0, default=2003, blank=False,
        verbose_name='X Examination Passing Year')
    passing_year_xii = models.DecimalField(
        max_digits=4, decimal_places=0, default=2003, blank=False,
        verbose_name='XII Examination Passing Year')
    gap_in_study = models.BooleanField(
        default=False, blank=True, verbose_name='Gap In Study')
    gap_reason = models.TextField(
        max_length=100, default="", blank=True, null=True,
        verbose_name='Reason For Gap In Study (Eg : JEE Preparation)')
    # this field was initially meant to store JEE Rank
    # but later on, for masters student GATE/JAM/etc. rank was needed.
    # So this field is now a "rank" field.
    # Do not get confused by name "jee_rank_field"
    jee_air_rank = models.DecimalField(
        max_digits=6, decimal_places=0, default=0, null=True, blank=False,
        verbose_name='JEE/GATE/JAM/Other Entrance Exam All India Rank ',
        validators=[MaxValueValidator(40000), MinValueValidator(1)],
        help_text="MA students should fill their clearance exam marks. Other "
                  "students should fill their clearance exam rank."
    )
    # since some students do not get a CML rank but get only category
    # rank, this field was added to accomodate those cases.
    rank_category = models.CharField(
        max_length=30, choices=RANK_CATEGORY, default='CML', blank=False,
        null=True, verbose_name='Rank Category',
        help_text='If your rank was not in CML (Common Merit List), then '
                  'select from Non-CML categories. MA students should select '
                  'MA Entrance Exam Marks.'
    )
    # physical disability status
    pd_status = models.CharField(
        max_length=50, choices=PD_STATUS, default='No Disability', null=True,
        blank=False, verbose_name='Physical Disability Status'
    )
    linkedin_link = models.URLField(
        max_length=254, blank=True, null=True,
        verbose_name='LinkedIn Account Public URL')
    # grades
    cpi = models.DecimalField(max_digits=4, decimal_places=2, blank=False,
                              default=0.00, verbose_name='CPI',
                              validators=[MaxValueValidator(10.0),
                                          MinValueValidator(0.0)])
    spi_1_sem = models.DecimalField(max_digits=4, decimal_places=2,
                                    blank=False, null=False, default=0.00,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(0.0)],
                                    verbose_name='SPI 1st Semester')
    spi_2_sem = models.DecimalField(max_digits=4, decimal_places=2,
                                    blank=False, null=False, default=0.00,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(0.0)],
                                    verbose_name='SPI 2nd Semester')
    spi_3_sem = models.DecimalField(max_digits=4, decimal_places=2,
                                    blank=False, null=False, default=0.00,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(0.0)],
                                    verbose_name='SPI 3rd Semester')
    spi_4_sem = models.DecimalField(max_digits=4, decimal_places=2,
                                    blank=False, null=False, default=0.00,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(0.0)],
                                    verbose_name='SPI 4th Semester')
    spi_5_sem = models.DecimalField(max_digits=4, decimal_places=2,
                                    blank=False, null=False, default=0.00,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(0.0)],
                                    verbose_name='SPI 5th Semester')
    spi_6_sem = models.DecimalField(max_digits=4, decimal_places=2,
                                    blank=False, null=False, default=0.00,
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

    # sitting for placement or intern
    job_candidate = models.BooleanField(default=False)
    intern_candidate = models.BooleanField(default=False)
    last_updated = models.DateTimeField(null=True, blank=False,
                                        verbose_name='Last Updated')

    class Meta:
        managed = True

    def __unicode__(self):
        return str(self.roll_no)

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        return super(Student, self).save(*args, **kwargs)

    def clean(self):
        if self.year or self.dept or self.prog or self.discipline:
            try:
                Programme.objects.get(year=int(self.year), dept=self.dept,
                                      name=self.prog, minor_status=False,
                                      discipline=self.discipline)
            except TypeError:
                raise ValidationError('No valid Major Programme '
                                      'found for given data.')
            except (ValueError, Programme.DoesNotExist):
                raise ValidationError('No valid programme '
                                      'found for given data.')
        else:
            raise ValidationError("Major Programme Fields "
                                  "cannot be left blank.")
        if self.minor_year or self.minor_dept or self.minor_prog or \
                self.minor_discipline:
            try:
                Programme.objects.get(year=int(self.minor_year),
                                      dept=self.minor_dept,
                                      name=self.minor_prog,
                                      discipline=self.minor_discipline,
                                      minor_status=True)
            except (ValueError, Programme.DoesNotExist):
                raise ValidationError('No valid Minor Programme '
                                      'found for given data.')


class Job(models.Model):
    company_owner = models.ForeignKey(Company, blank=True, null=True,
                                      verbose_name='Company Owner')
    # Fields Needed
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Job Description')
    designation = models.CharField(blank=True, max_length=90, null=True,
                                   verbose_name='Job Designation')
    profile_name = models.CharField(max_length=50, null=True,
                                    verbose_name='Profile Name')
    num_openings = models.DecimalField(max_digits=3, decimal_places=0,
                                       null=True, blank=False,
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
                                    default=0.00, null=True, blank=True,
                                    verbose_name='B.Tech/B.Des CTC/year')
    ctc_mtech = models.DecimalField(max_digits=16, decimal_places=2,
                                    default=0.00, null=True,
                                    blank=True,
                                    verbose_name='M.Tech/M.Des CTC/year')
    ctc_msc = models.DecimalField(max_digits=16, decimal_places=2,
                                  default=0.00, null=True,
                                  blank=True, verbose_name='M.Sc. CTC/year')
    ctc_ma = models.DecimalField(max_digits=16, decimal_places=2,
                                 default=0.00, null=True,
                                 blank=True, verbose_name='M.A. CTC/year')
    ctc_phd = models.DecimalField(max_digits=16, decimal_places=2,
                                  default=0.00, null=True,
                                  blank=True, verbose_name='Ph.D. CTC/year')
    ctc_msr = models.DecimalField(max_digits=16, decimal_places=2,
                                  default=0.00, null=True,
                                  blank=True, verbose_name='MS(R) CTC/year')
    gross_btech = models.DecimalField(max_digits=16, decimal_places=2,
                                      default=0.00, null=True,
                                      blank=True,
                                      verbose_name='B.Tech/B.Des Gross Salary')
    gross_mtech = models.DecimalField(max_digits=16, decimal_places=2,
                                      default=0.00, null=True,
                                      blank=True,
                                      verbose_name='M.Tech/M.Des Gross Salary')
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
    gross_msr = models.DecimalField(max_digits=16, decimal_places=2,
                                    default=0.00, null=True,
                                    blank=True,
                                    verbose_name='MS(R) Gross Salary')
    additional_info = models.TextField(blank=True, null=True, default="",
                                       verbose_name='Additional Information '
                                                    'About Salary (if any)')
    # Job description
    bond_link = models.FileField(null=True, blank=True,
                                 upload_to=get_bond_link_name,
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
    opening_datetime = models.DateTimeField(blank=True, null=True,
                                            verbose_name='Opening Date')
    application_deadline = models.DateTimeField(blank=True, null=True,
                                                verbose_name='Closing Date')

    class Meta:
        managed = True

    def __unicode__(self):
        return str(self.designation) + " (" + str(self.company_owner.company_name) + ")"

    def save(self, *args, **kwargs):
        if not self.id:
            self.posted_on = timezone.now()
            self.opening_datetime = timezone.now() + timedelta(days=30)
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

    # debar student from participating in a particular job
    is_debarred = models.BooleanField(default=False)

    stud = models.ForeignKey(Student, null=True, blank=True)
    job = models.ForeignKey(Job, null=True, blank=True)
    creation_datetime = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'Student-Job-Relation'
        verbose_name_plural = 'Students-Job-Relations'

    def __unicode__(self):
        return str(self.stud.name) + " " + str(self.job)

    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_datetime = timezone.now()
        return super(StudentJobRelation, self).save(*args, **kwargs)


class Event(models.Model):
    company_owner = models.ForeignKey(Company, null=True, blank=True)
    title = models.CharField(max_length=50, null=True,
                             verbose_name='Event Title')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE,null=True,
                                  verbose_name='Event Type',
                                  help_text='Select event type from the '
                                            'dropdown menu.')
    duration = models.DecimalField(default=1, max_digits=4, decimal_places=2,
                                   verbose_name="Estimated Duration (in "
                                                "hours)")
    logistics = models.CharField(null=True, blank=True, max_length=400,
                                 verbose_name="Logistics")
    remark = models.CharField(max_length=400, null=True, blank=True,
                              verbose_name='Remark (Optional)')
    final_date = models.DateField(null=True, blank=True,
                                  verbose_name='Approved Date',
                                  help_text="This is the date assigned for "
                                            " the event by the administrator.")
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
    avatar = VersatileImageField(upload_to=get_avatar_name,
                                 blank=False, null=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Avatar'
        verbose_name_plural = 'Avatars'

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(Avatar, self).save(*args, **kwargs)

    def image_tag(self):
        return format_html(
            '<img src="%s" width="200" height="200" />' % self.avatar.url)

    def stud_name(self):
        return self.stud.name

    image_tag.short_description = 'Avatar Image'


class Signature(models.Model):
    stud = models.OneToOneField(Student, on_delete=models.CASCADE,
                                null=True)
    signature = VersatileImageField(upload_to=get_sign_name, blank=False,
                                    null=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Signature'
        verbose_name_plural = 'Signatures'

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(Signature, self).save(*args, **kwargs)

    def image_tag(self):
        return format_html(
            '<img src="%s" width="200" height="200" />' % self.signature.url)

    def stud_name(self):
        return self.stud.name

    image_tag.short_description = 'Signature Image'


class CV(models.Model):
    stud = models.OneToOneField(Student, null=True, on_delete=models.CASCADE)
    cv1 = models.FileField(upload_to=get_cv1_name, blank=True, null=True)
    cv2 = models.FileField(upload_to=get_cv2_name, blank=True, null=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Curriculum Vitae'
        verbose_name_plural = 'Curriculum Vitae'

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(CV, self).save(*args, **kwargs)


class ProgrammeJobRelation(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    prog = models.ForeignKey(Programme, null=True,
                             on_delete=models.CASCADE)

    def get_year(self):
        return self.prog.year

    def get_dept(self):
        return self.prog.dept

    def get_minor_status(self):
        return 'Yes' if self.prog.minor_status else 'No'

    get_year.short_description = 'year'
    get_dept.short_description = 'department'
    get_minor_status.short_description = 'Major/Minor'

    class Meta:
        verbose_name = 'Programme-Job-Relation'
        verbose_name_plural = 'Programme-Job-Relations'

    def __unicode__(self):
        return str(self.prog.name)


class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title', null=True,
                             blank=True)
    category = models.CharField(max_length=25, verbose_name='Category',
                                null=True, blank=True)
    detail = models.TextField(max_length=1000, verbose_name='Detail',
                              null=True, blank=True)
    hide = models.BooleanField(default=True, blank=True)
    creation_datetime = models.DateTimeField(null=True, blank=True,
                                             verbose_name='Created On')
    last_updated = models.DateTimeField(null=True, blank=True,
                                        verbose_name='Last Updated On')

    def save(self, **kwargs):
        if not self.id:
            self.creation_datetime = timezone.now()
        self.last_updated = timezone.now()
        super(Announcement, self).save(**kwargs)
