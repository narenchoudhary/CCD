from django.forms import ModelForm, inlineformset_factory, Textarea

from models import *


InternProgFormSet = inlineformset_factory(
    IndInternship,
    ProgrammeInternRelation,
    fields=('prog',),
    extra=10
)


class RecruiterAddInternShip(ModelForm):
    class Meta:
        model = IndInternship
        fields = ['designation', 'description', 'stipend', 'profile',
                  'duration']
        widgets = {
            'description': Textarea(attrs=dict(rows=4, cols=15))
        }


class AdminEditInternShip(ModelForm):
    class Meta:
        model = IndInternship
        exclude = ['company_owner', 'posted_on', 'last_updated',
                   'approved_on']
