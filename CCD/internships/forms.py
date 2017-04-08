from django import forms

from .models import IndustrialInternship


class CompanyInternshipForm(forms.ModelForm):
    """
    ``IndustrialInternship`` modelform for Company users.
    """

    class Meta:
        model = IndustrialInternship
        fields = ['description', 'designation', 'profile', 'currency',
                  'stipend', 'duration', 'start_date', 'end_date',
                  'backlog_filter', 'max_backlog_allowed', 'cpi_shortlist',
                  'minimum_cpi', 'percentage_x', 'percentage_xii']


class AdminInternshipForm(forms.ModelForm):
    """
    ``IndustrialInternship`` modelform for Admin users.
    """

    class Meta:
        model = IndustrialInternship
        fields = ['description', 'designation', 'profile', 'currency',
                  'stipend', 'duration', 'start_date', 'end_date',
                  'backlog_filter', 'max_backlog_allowed', 'cpi_shortlist',
                  'minimum_cpi', 'percentage_x', 'percentage_xii',
                  'opening_datetime', 'closing_datetime']
