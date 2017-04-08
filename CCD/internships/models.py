from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from jobportal.models import Programme, Student, Company


@python_2_unicode_compatible
class IndustrialInternship(models.Model):
    """
    Model class representing industrial internships posted by
    Company user.
    """
    company_owner = models.ForeignKey(Company, verbose_name=_('Company Owner'))
    description = models.CharField(max_length=600,
                                   verbose_name=_('Intership Description'))
    designation = models.CharField(max_length=50)
    profile = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    stipend = models.IntegerField()
    duration = models.IntegerField(
        verbose_name=_('Internship Duration (in months)'))
    start_date = models.DateField(verbose_name=_('Tentative Start Date'))
    end_date = models.DateField(verbose_name=_('Tentative Completion Date'))
    # requirements
    backlog_filter = models.BooleanField(
        default=False, blank=True, verbose_name=_('Backlog Filtering'))
    max_backlog_allowed = models.IntegerField(
        default=1, blank=True, verbose_name=_('Number of backlogs permitted'))
    cpi_shortlist = models.BooleanField(
        default=False, blank=True, verbose_name=_('CPI Filtering'))
    minimum_cpi = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, default=5.0,
        verbose_name=_('CPI Filtering')
    )
    percentage_x = models.DecimalField(
        max_length=5, decimal_places=2, blank=True, default=60.00,
        verbose_name=_('Percentage X')
    )
    percentage_xii = models.DecimalField(
        max_length=5, decimal_places=2, blank=True, default=60.00,
        verbose_name=_('Percentage XII')
    )
    # Dates and Approvals
    posted_on = models.DateTimeField()
    last_updated = models.DateTimeField()
    approved = models.NullBooleanField(default=None)
    approved_on = models.DateTimeField(null=True)
    opening_datetime = models.DateTimeField()
    closing_datetime = models.DateTimeField()

    def __str__(self):
        return self.designation

    @property
    def deadline_passed(self):
        """
        Property for checking if ``closing_datetime`` has passed.
        :return: True if ``closing_datetime`` has passed
        :rtype: bool
        """
        return timezone.now() > self.closing_datetime

    @property
    def opened(self):
        """
        Property for checking if ``opening_datetime`` has passed.
        :return: True if ``opening_datetime`` has passed.
        :rtype: bool
        """
        return timezone.now() > self.closing_datetime

    @property
    def can_apply(self):
        """
        Property for checking if an eligible student can apply for
        job at a given point of time.
        :return True if student can apply otherwise False
        :rtype: bool
        """
        return self.opened and not self.deadline_passed

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.id:
            self.posted_on = now
            self.opening_date = now + timezone.timedelta(days=60)
            self.closing_date = now + timezone.timedelta(days=90)
        self.last_updated = now
        super(IndustrialInternship, self).save(*args, **kwargs)


@python_2_unicode_compatible
class StudentInternRelation(models.Model):
    stud = models.ForeignKey(Student)
    intern = models.ForeignKey(IndustrialInternship)
    shortlist_init = models.BooleanField(default=False)
    intern_init = models.BooleanField(default=False)
    intern_approved = models.NullBooleanField(default=None)
    is_debarred = models.BooleanField(default=False)
    cv1 = models.BooleanField(default=False)
    cv2 = models.BooleanField(default=False)

    created_on = models.DateTimeField()

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = timezone.now()
        super(StudentInternRelation, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('stud', 'intern')


@python_2_unicode_compatible
class ProgrammeInternRelation(models.Model):
    intern = models.ForeignKey(IndustrialInternship)
    prog = models.ForeignKey(Programme, null=True)

    def __str__(self):
        return str(self.intern.designation)

    class Meta:
        unique_together = ('intern', 'prog')
