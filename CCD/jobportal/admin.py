from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import *


class UserProfileChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserProfile


class UserProfileCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserProfile


class UserProfileAdmin(UserAdmin):
    form = UserProfileChangeForm
    add_form = UserProfileCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'login_server')}),
    )
    list_display = ('username', 'user_type', 'is_active', 'stud_programme')
    list_filter = ('user_type', 'is_active')


class ComanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'website', 'head_hr_name',
                    'head_hr_mobile')
    list_display_links = ('company_name', 'website')
    list_filter = ('approved',)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no', 'year', 'dept', 'prog', 'minor_dept')
    list_filter = ('year', 'dept', 'prog', 'minor_year', 'category', 'sex',
                   'placed', 'ppo')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('year', 'dept', 'dept_code')


class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('year', 'dept', 'discipline', 'name', 'minor_status',
                    'open_for_placement', 'open_for_internship')
    list_filter = ('minor_status', 'open_for_placement', 'open_for_internship'
                   , 'name')


class EventAdmin(admin.ModelAdmin):
    list_display = ('company_owner', 'title', 'duration', 'final_date',
                    'is_approved')
    list_filter = ('is_approved',)


class JobAdmin(admin.ModelAdmin):
    list_display = ('company_owner', 'designation', 'profile_name',
                    'opening_datetime', 'application_deadline', 'approved')
    list_filter = ('cpi_shortlist', 'backlog_filter', 'approved')


class ProgrammeJobRelationAdmin(admin.ModelAdmin):
    model = ProgrammeJobRelation
    list_display = ('job', 'get_year', 'get_dept', 'prog', 'get_minor_status')


class StudentJobRelationAdmin(admin.ModelAdmin):
    list_display = ('stud', 'shortlist_init', 'placed_init',
                    'placed_approved',)
    list_filter = ('shortlist_init', 'placed_init', 'placed_approved')


class AvatarAdmin(admin.ModelAdmin):
    model = Avatar
    list_display = ('stud', 'stud_name', 'last_updated', )
    readonly_fields = ('image_tag', 'stud_name')


class SignatureAdmin(admin.ModelAdmin):
    model = Signature
    list_display = ('stud', 'stud_name', 'last_updated')
    readonly_fields = ('image_tag', 'stud_name')


class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'position')



admin.site.register(SiteManagement)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(Company, ComanyAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Alumni)

admin.site.register(Job, JobAdmin)
admin.site.register(StudentJobRelation, StudentJobRelationAdmin)
admin.site.register(ProgrammeJobRelation, ProgrammeJobRelationAdmin)

admin.site.register(Programme, ProgrammeAdmin)

admin.site.register(Avatar, AvatarAdmin)
admin.site.register(Signature, SignatureAdmin)
admin.site.register(CV)

admin.site.register(Event, EventAdmin)
