from django.db import models
from jobportal.models import Alumni, Student
from datetime import datetime


class ResearchProposal(models.Model):
    alum_owner = models.ForeignKey(Alumni, blank=True, null=True)
    alum_current_institute = models.TextField(null=True, blank=True, verbose_name="Alumni Current Institute")
    alum_current_address = models.TextField(null=True, blank=True, verbose_name="Alumni Address")
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True,
                                   verbose_name="Duration in Months")
    hours_week = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True,
                                     verbose_name="Estimated Hours/Week")
    prerequsites = models.TextField(max_length=200, blank=True, null=True)
    outcome = models.TextField(max_length=200, blank=True, null=True)
    added = models.DateTimeField(default=datetime.now, blank=True, null=True)
    last_updated = models.DateTimeField(default=datetime.now, blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True)
    deleted_on = models.DateTimeField(blank=True, default=datetime.now)
    applicants = models.ManyToManyField(Student, through="StudentProposalRelation")

    class Meta:
        managed = True

    def __unicode__(self):
        return str(self.title)


class StudentProposalRelation(models.Model):
    proposal = models.ForeignKey(ResearchProposal, null=True)
    stud = models.ForeignKey(Student, blank=True, null=True)
    writeup = models.TextField(max_length=500)
    max_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    opt_out = models.BooleanField(default=False, blank=True)
    opt_out_date = models.DateTimeField(blank=True, null=True)
    date_applied = models.DateTimeField(blank=True, null=True)
    # Reporting related fields
    report_byAlum = models.BooleanField(default=False)
    report_byAlum_reasons = models.TextField()
    report_byAlum_date = models.DateField(blank=True, null=True)
    report_byStud = models.BooleanField(default=False)
    report_byStud_reasons = models.TextField()
    report_byStud_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True

    def __unicode__(self):
        return str(self.max_hours)
