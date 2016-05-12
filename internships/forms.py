from django.core.exceptions import ValidationError
from django.forms import ModelForm, inlineformset_factory
from functools import partial
# Project imports
from models import *
# Crispy Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

InternProgFormSet = inlineformset_factory(IndInternship, ProgrammeInternRelation, fields=('year', 'dept', 'prog'),
                                          extra=10)


class RecruiterAddInternShip(ModelForm):
    class Meta:
        model = IndInternship
        fields = ['designation', 'description', 'stipend', 'profile', 'duration']


class AdminEditInternShip(ModelForm):
    class Meta:
        model = IndInternship
        exclude = ['company_owner', 'posted_on', 'last_updated', 'approved_on']
