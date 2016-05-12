from django.contrib import admin
# Register your models here.
from .models import *


admin.site.register(UserProfile)

admin.site.register(Admin)
admin.site.register(CompanyReg)
admin.site.register(Company)
admin.site.register(Student)
admin.site.register(Alumni)

admin.site.register(Job)
admin.site.register(StudentJobRelation)

admin.site.register(Year)
admin.site.register(Department)
admin.site.register(Programme)


class EventAdmin(admin.ModelAdmin):
    fields = ['alum_owner', 'company_owner', 'title', 'date1', 'date2', 'date3', 'final_date', 'finalised']
    list_display = ['alum_owner', 'company_owner', 'title', 'date1', 'date2', 'date3', 'final_date', 'finalised']


admin.site.register(Event, EventAdmin)
