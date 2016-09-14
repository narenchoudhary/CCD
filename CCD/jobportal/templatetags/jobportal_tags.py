from django import template
from django.utils import timezone, dateparse

from jobportal.models import SiteManagement

register = template.Library()


@register.simple_tag
def date_passed(value):
    """
    Returns True if deadline has passed
    :param value: Query sting for which deadline status is needed
    :return: True/False
    """
    site_management = SiteManagement.objects.all()[0]
    now = timezone.now()
    if value is 'job_stud_sign':
        return site_management.job_student_sign_update_deadline < now
    elif value == 'job_stud_avatar':
        return site_management.job_student_avatar_update_deadline < now
    elif value == 'job_stud_profile':
        return site_management.job_student_profile_update_deadline < now
    elif value == 'job_stud_cv':
        return site_management.job_student_cv_update_deadline < now
    elif value == 'intern_stud_sign':
        return site_management.intern_student_sign_update_deadline < now
    elif value == 'intern_stud_avatar':
        return site_management.intern_student_avatar_update_deadline < now
    elif value == 'intern_stud_cv':
        return site_management.intern_student_cv_update_deadline < now
    elif value == 'intern_stud_profile':
        return site_management.intern_student_profile_update_deadline < now
    else:
        return True
