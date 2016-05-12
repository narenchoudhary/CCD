from django.db import models
from jobportal.models import Alumni, Company


class AlumJob(models.Model):
    AUDIENCE_CHOICES = (
        ('young', 'Young Alumni'),
        ('old', 'Older Alumni'),
        ('all', 'All Alumni')
    )
    company_owner = models.ForeignKey(Company, null=False)
    designation = models.CharField(max_length=20, blank=False, null=False)
    description = models.TextField(max_length=200, blank=True, null=True)
    profile_name = models.CharField(max_length=20, null=False, blank=False)
    audience = models.CharField(max_length=6, choices=AUDIENCE_CHOICES)
    approved = models.NullBooleanField(default=None)
    approved_on = models.DateTimeField(null=True, blank=True)
    posted_on = models.DateTimeField()
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()

    def __unicode__(self):
        return str(self.designation)


# TODO: Ask Prarthana for guidelines
class AlumJobRelation(models.Model):
    # status variables
    placed_init = models.BooleanField(default=False)
    shortlist_status = models.BooleanField(default=False)
    alum = models.ForeignKey(Alumni, null=True, blank=True)
    job = models.ForeignKey(AlumJob, null=True, blank=True)

    def __unicode__(self):
        return str(self.id)