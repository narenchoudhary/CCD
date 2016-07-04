from django.contrib import admin

from .models import *

admin.site.register(UserProfile)

admin.site.register(Admin)
admin.site.register(Company)
admin.site.register(Student)
admin.site.register(Alumni)

admin.site.register(Job)
admin.site.register(StudentJobRelation)

admin.site.register(Year)
admin.site.register(Department)
admin.site.register(Programme)

admin.site.register(Avatar)
admin.site.register(Signature)
admin.site.register(CV)

admin.site.register(Event)
