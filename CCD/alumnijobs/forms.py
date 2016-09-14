from django import forms
from alumnijobs.models import AlumJob


class CompanyAddAlumJob(forms.ModelForm):
    class Meta:
        model = AlumJob
        fields = ['designation', 'description', 'profile_name', 'audience']


class AdminEditAlumJob(forms.ModelForm):
    class Meta:
        model = AlumJob
        exclude = ['company_owner']
