from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import *

admin.site.site_header = 'CCD administration'


class UserProfileChangeForm(UserChangeForm):
    """
    Form for creating User Profile instances.
    """
    class Meta(UserChangeForm.Meta):
        model = UserProfile


class UserProfileCreationForm(UserCreationForm):
    """
    Subclass of UserCreationForm used for add_form field
    """
    class Meta(UserCreationForm.Meta):
        model = UserProfile


class UserProfileAdmin(UserAdmin):
    """
    Class that represents UserProfile model in the admin interface.
    """
    form = UserProfileChangeForm
    add_form = UserProfileCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'login_server')}),
    )
    list_display = ('username', 'user_type', 'is_active', 'stud_programme')
    list_filter = ('user_type', 'is_active')
    search_fields = ('username',)


class CompanyAdmin(admin.ModelAdmin):
    """
    Class that represents Company model in the admin interface.
    """
    list_display = ('company_name', 'website', 'head_hr_name',
                    'head_hr_mobile')
    list_display_links = ('company_name', 'website')
    list_filter = ('approved',)
    search_fields = ('company_name', 'website')


class StudentAdmin(admin.ModelAdmin):
    """
    Class that represents Student model in the admin interface.
    """
    list_display = ('name', 'roll_no', 'year', 'dept', 'prog', 'minor_dept')
    list_filter = ('year', 'dept', 'prog', 'minor_year', 'category', 'sex',
                   'placed', 'ppo')
    search_fields = ('name', 'roll_no')


class ProgrammeAdmin(admin.ModelAdmin):
    """
    Class that represents Programme model in the admin interface.
    """
    list_display = ('year', 'dept', 'discipline', 'name', 'minor_status',
                    'open_for_placement', 'open_for_internship')
    list_filter = ('minor_status', 'open_for_placement', 'open_for_internship',
                   'name')
    search_fields = ('discipline',)


class EventAdmin(admin.ModelAdmin):
    """
    Class that represents Event model in the admin interface.
    """
    list_display = ('company_owner', 'title', 'duration', 'final_date',
                    'is_approved')
    list_filter = ('is_approved',)


class JobAdmin(admin.ModelAdmin):
    """
    Class that represents Job model in the admin interface.
    """
    list_display = ('company_owner', 'designation', 'profile_name',
                    'opening_datetime', 'application_deadline', 'approved')
    list_filter = ('cpi_shortlist', 'backlog_filter', 'approved')
    search_fields = ('company_owner', 'designation')


class ProgrammeJobRelationAdmin(admin.ModelAdmin):
    """
    Class that represents ProgrammeJobRelation model in the admin interface.
    """
    model = ProgrammeJobRelation
    list_display = ('job', 'get_year', 'get_dept', 'prog', 'get_minor_status')


class StudentJobRelationAdmin(admin.ModelAdmin):
    """
    Class that represents StudentJobRelation model in the admin interface.
    """
    model = StudentJobRelation
    list_display = ('stud', 'shortlist_init', 'placed_init',
                    'placed_approved', 'cv1', 'cv2')
    list_filter = ('shortlist_init', 'placed_init', 'placed_approved')
    search_fields = (
        'stud__roll_no', 'stud__name', 'job__designation',
        'job__company_owner__company_name'
    )
    ordering = ('creation_datetime', 'cv1', 'cv2')
    actions = ['shortlist_init_true', 'shortlist_init_false',
               'placed_init_true', 'placed_init_false']

    def shortlist_init_true(self, request, queryset):
        """
        Action method for shortlisting selected StudentJobRelation instances
        :param request:
        :param queryset:
        :return:
        """
        rows_updated = queryset.update(shortlist_init=True)
        if rows_updated == 1:
            message_bit = '1 applicant was'
        else:
            message_bit = '%s applicants were' % rows_updated
        self.message_user(
            request, '%s successfully marked as shortlisted.' % message_bit)

    shortlist_init_true.short_description = \
        'Add selected StudentsJobRelations(s) to shortlist'

    def shortlist_init_false(self, request, queryset):
        """
        Action method for un-shortlisting selected StudentJobRelation instances
        :param request:
        :param queryset:
        :return:
        """
        rows_updated = queryset.update(shortlist_init=False)
        if rows_updated == 1:
            message_bit = '1 applicant was'
        else:
            message_bit = '%s applicants were' % rows_updated
        self.message_user(
            request, '%s successfully removed from shortlist.' % message_bit)

    shortlist_init_false.short_description = \
        'Remove selected StudentsJobRelations(s) from shortlist'

    def placed_init_true(self, request, queryset):
        """
        Action method for initiating placement request for selected
        StudentJobRelation instances
        :param request:
        :param queryset:
        :return:
        """
        rows_updated = queryset.update(placed_init=True)
        if rows_updated == 1:
            message_bit = '1 applicant'
        else:
            message_bit = '%s applicants' % rows_updated
        self.message_user(
            request, 'Placement request initiated for %s' % message_bit)

    placed_init_true.short_description = \
        'Initiate placement request for selected StudentsJobRelations(s)'

    def placed_init_false(self, request, queryset):
        """
        Action method for cancelling placement request for selected
        StudentJobRelation instances
        :param request:
        :param queryset:
        :return:
        """
        rows_updated = queryset.update(placed_init=False)
        if rows_updated == 1:
            message_bit = '1 applicant'
        else:
            message_bit = '%s applicants' % rows_updated
        self.message_user(
            request, 'Placement request cancelled for %s' % message_bit)

    placed_init_false.short_description = \
        'Cancel placement request for selected StudentsJobRelations(s)'


class AvatarAdmin(admin.ModelAdmin):
    """
    Class that represents Avatar model in the admin interface.
    """
    model = Avatar
    list_display = ('stud', 'stud_name', 'last_updated', )
    readonly_fields = ('image_tag', 'stud_name')
    search_fields = ('stud__name', 'stud__roll_no')


class SignatureAdmin(admin.ModelAdmin):
    """
    Class that represents Signature model in the admin interface.
    """
    model = Signature
    list_display = ('stud', 'stud_name', 'last_updated')
    readonly_fields = ('image_tag', 'stud_name')
    search_fields = ('stud__name', 'stud__roll_no')


class CVAdmin(admin.ModelAdmin):
    """
    Class that represents CV model in the admin interface.
    """
    model = CV
    list_display = ('stud', 'last_updated')
    search_fields = ('stud__name', 'stud__roll_no')


class AdminAdmin(admin.ModelAdmin):
    """
    Class that represents Admin model in the admin interface.
    """
    list_display = ('user', 'position')


class AnnouncementAdmin(admin.ModelAdmin):
    """
    Class that represents Announcement model in the admin interface.
    """
    model = Announcement
    list_display = ('title', 'category', 'hide', 'last_updated')
    list_filter = ('category', 'hide')
    actions = ['hide_announcement']

    def hide_announcement(self, request, queryset):
        rows_updated = queryset.update(hide=True)
        if rows_updated == 1:
            message_bit = '1 Announcement was'
        else:
            message_bit = '%s Announcements were' % rows_updated
        message = 'Status of %s successfully updated to hidden.' % message_bit
        self.message_user(request, message)

    hide_announcement.short_description = 'Mark selected Announcement(s) ' \
                                          'as hidden'

admin.site.register(SiteManagement)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Student, StudentAdmin)

admin.site.register(Job, JobAdmin)
admin.site.register(StudentJobRelation, StudentJobRelationAdmin)
admin.site.register(ProgrammeJobRelation, ProgrammeJobRelationAdmin)

admin.site.register(Programme, ProgrammeAdmin)

admin.site.register(Avatar, AvatarAdmin)
admin.site.register(Signature, SignatureAdmin)
admin.site.register(CV, CVAdmin)

admin.site.register(Event, EventAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
