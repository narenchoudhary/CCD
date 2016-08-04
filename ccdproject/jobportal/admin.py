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
        (None, {'fields': ('user_type',)}),
    )


admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(Admin)
admin.site.register(Company)
admin.site.register(Student)
admin.site.register(Alumni)

admin.site.register(Job)
admin.site.register(StudentJobRelation)
admin.site.register(ProgrammeJobRelation)
admin.site.register(MinorProgrammeJobRelation)

admin.site.register(Year)
admin.site.register(Department)
admin.site.register(Programme)

admin.site.register(Avatar)
admin.site.register(Signature)
admin.site.register(CV)

admin.site.register(Event)
