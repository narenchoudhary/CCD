from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import Tab, TabHolder
from datetime import datetime


# For Alumni: Add new proposal
class AddProposal(forms.Form):
    alum_current_institute = forms.CharField(max_length=50, required=True)
    alum_current_address = forms.CharField(widget=forms.Textarea, required=True, max_length=100)
    title = forms.CharField(max_length=60, required=True,
                            # help_text="Please choose title carefully.Title cannot be changed later.",
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Eg. Analysis of Support Vector Machine Models'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'A short description of the project.'}),
                                  label="Description", max_length=200, required=True)
    duration = forms.DecimalField(decimal_places=2, max_digits=4, required=True, label="Estimated Duration(in months)")
    hours_week = forms.DecimalField(decimal_places=1, max_digits=2, required=True, label="Estimated Hours/Week")
    prerequsites = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Eg. Expertise in Java'}),
                                   label="Prerequisites", max_length=200, required=True)
    outcome = forms.CharField(required=True,
                              widget=forms.TextInput(attrs={'placeholder': "Eg. Research Proposal, Software Package"}))

    def __init__(self, *args, **kwargs):
        super(AddProposal, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Alumni Information',
                    'alum_current_institute',
                    'alum_current_address'
                ),
                Tab(
                    'Proposal Details',
                    'title',
                    'description',
                    'duration',
                    'hours_week',
                    'prerequsites',
                    'outcome'
                )
            )
        )


# For Alumni: Edit Proposal
class EditProposal(AddProposal):
    title = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    alum_current_institute = forms.CharField(max_length=50, required=True,
                                             widget=forms.TextInput(attrs={'readonly': 'readonly'}))


# For Students: Apply to a proposal
class StudApply(forms.Form):
    max_hours = forms.DecimalField(max_digits=2, decimal_places=1, required=True, label="Hours/Week",
                                   help_text="Maximum hours/week you can give.")
    writeup = forms.CharField(widget=forms.Textarea, required=True,
                              help_text="Please write it carefully. It can be submitted only once.")


# Report
class ReportForm(forms.Form):
    reasons = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Put your complaint here.'}),
                              label="Reasons", max_length=200, required=True,
                              help_text="Please be clear and specific.")
