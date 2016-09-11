from django import template
from django.utils import timezone

from jobportal.models import SiteManagement

register = template.Library()


@register.filter(expects_localtime=True, is_safe=True)
def date_passed(value):
    try:
        print value
        return value < timezone.now().date()
    except ValueError:
        return True


@register.simple_tag(name='job_student_profile_update_deadline_passed')
def job_student_profile_update_deadline():
    site_management = SiteManagement.objects.all()[0]
    now = timezone.now()
    return site_management.job_student_profile_update_deadline < now


@register.simple_tag(name='job_student_cv_update_deadline_passed')
def job_student_cv_update_deadline():
    site_management = SiteManagement.objects.all()[0]
    now = timezone.now()
    return site_management.job_student_cv_update_deadline < now


@register.simple_tag(name='job_student_avatar_update_deadline_passed')
def job_student_avatar_update_deadline():
    site_management = SiteManagement.objects.all()[0]
    now = timezone.now()
    return site_management.job_student_avatar_update_deadline < now


@register.simple_tag(name='job_student_sign_update_deadline_passed')
def job_student_sign_update_deadline():
    site_management = SiteManagement.objects.all()[0]
    now = timezone.now()
    return site_management.job_student_sign_update_deadline < now
