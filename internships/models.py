from django.db import models
from jobportal.models import Year, Department, Programme, Student, Company
from smart_selects.db_fields import ChainedForeignKey
import datetime
# Create your models here.


class IndInternship(models.Model):
    company_owner = models.ForeignKey(Company)
    description = models.CharField(max_length=200)
    designation = models.CharField(max_length=20)
    profile = models.CharField(max_length=10)
    stipend = models.IntegerField()
    duration = models.IntegerField()
    # Dates and Approvals
    posted_on = models.DateTimeField()
    last_updated = models.DateTimeField()
    approved = models.NullBooleanField(default=None)
    approved_on = models.DateTimeField(null=True)
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()

    def __unicode__(self):
        return self.designation


class StudentInternRelation(models.Model):
    stud = models.ForeignKey(Student)
    intern = models.ForeignKey(IndInternship)
    round = models.IntegerField(default=1)
    shortlist_init = models.BooleanField(default=False)
    shortlist_approved = models.NullBooleanField(default=None)
    intern_init = models.BooleanField(default=False)
    intern_approved = models.NullBooleanField(default=None)
    ppo_init = models.BooleanField(default=False)
    ppo_approved = models.NullBooleanField(default=None)
    dropped = models.BooleanField(default=False)
    cv1 = models.BooleanField(default=False)
    cv2 = models.BooleanField(default=False)

    def __unicode__(self):
        return self.stud.first_name


class ProgrammeInternRelation(models.Model):
    intern = models.ForeignKey(IndInternship)
    year = models.ForeignKey(Year, null=True)
    dept = ChainedForeignKey(Department, chained_field='year', chained_model_field='year', show_all=False, null=True)
    prog = ChainedForeignKey(Programme, chained_field='dept', chained_model_field='dept', show_all=False, null=True)

    def __unicode__(self):
        return self.intern.designation
