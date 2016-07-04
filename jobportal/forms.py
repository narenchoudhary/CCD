from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, ModelForm, inlineformset_factory

from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

from models import *
from widgets import CheckBoxBootstrapSwitch
from django.conf import settings


class CustomJobProgFormSet(BaseInlineFormSet):

    def clean(self):
        super(CustomJobProgFormSet, self).clean()

JobProgFormSet = inlineformset_factory(
    Job, ProgrammeJobRelation,
    fields=('year', 'dept', 'prog'), extra=10, formset=CustomJobProgFormSet)


JobProgMinorFormSet = inlineformset_factory(Job, MinorProgrammeJobRelation,
                                            fields=('year', 'dept', 'prog'), extra=10)


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Webmail', max_length=25)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class EditStudProfileForm(ModelForm):

    class Meta:
        model = Student
        exclude = ['user', 'placed', 'intern2', 'intern3', 'ppo']

    def __init__(self, *args, **kwargs):
        super(EditStudProfileForm, self).__init__(*args, **kwargs)
        self.fields['roll_no'].disabled = True
        self.fields['iitg_webmail'].disabled = True
        self.fields['first_name'].disabled = True
        self.fields['middle_name'].disabled = True
        self.fields['last_name'].disabled = True
        self.fields['year'].disabled = True
        self.fields['dept'].disabled = True
        self.fields['prog'].disabled = True
        self.fields['minor_year'].disabled = True
        self.fields['minor_dept'].disabled = True
        self.fields['minor_prog'].disabled = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Student Information',
                    'roll_no', 'iitg_webmail',
                    'first_name', 'middle_name', 'last_name', 'dob',
                    'sex', 'category', 'nationality', 'year', 'dept',
                    'prog', 'minor_year', 'minor_dept', 'minor_prog',
                    'hostel', 'room_no'
                ),
                Tab(
                    'Contact Information',
                    PrependedText('linkedin_link', 'https://'), 'alternative_email',
                    'mobile_campus', 'mobile_campus_alternative', 'mobile_home'
                ),
                Tab(
                    'Home Address',
                    'address_line1', 'address_line2',
                    'address_line3', 'pin_code'
                ),
                Tab(
                    'Academic',
                    'jee_air_rank', 'percentage_x', 'percentage_xii',
                    'board_x', 'board_xii', 'medium_x', 'medium_xii', 'passing_year_x',
                    'passing_year_xii', 'gap_in_study', 'gap_reason',
                ),
                Tab(
                    'CPI',
                    'cpi', 'spi_1_sem', 'spi_2_sem', 'spi_3_sem',
                    'spi_4_sem', 'spi_5_sem', 'spi_6_sem',
                )
            )
        )

    def clean(self):
        cleaned_data = super(EditStudProfileForm, self).clean()
        minor_y = bool(cleaned_data.get('minor_year'))
        minor_d = bool(cleaned_data.get('minor_dept'))
        minor_p = bool(cleaned_data.get('minor_prog'))
        check_all = minor_y and minor_d and minor_p
        check_none = not(minor_y or minor_d or minor_p)
        if not(check_all or check_none):
            raise forms.ValidationError("Minor programme errors")

        year = bool(cleaned_data.get('year'))
        dept = bool(cleaned_data.get('dept'))
        prog = bool(cleaned_data.get('prog'))
        check_all = year and dept and prog
        check_none = not(year or dept or prog)
        if not(check_all or check_none):
            raise forms.ValidationError("Programme errors")


class CompanyJobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ['alum_owner', 'company_owner', 'posted_by_alumnus', 'posted_by_company',
                   'posted_on', 'approved', 'approved_on', 'last_updated', 'opening_date',
                   'application_deadline']

    def __init__(self, *args, **kwargs):
        super(CompanyJobForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['bond_link'].help_text = 'Upload bond document to Drive/Dropbox and add link here.'
        self.fields['bond_link'].label = 'URL of bond document'
        self.fields['cpi_shortlist'].label = 'CPI Shortlist'
        self.fields['cpi_shortlist'].help_text = 'Select this if CPI filtering is needed.'
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Basic Information',
                    Field('description', placeholder='Brief Description of what does consists of ...'),
                    Field('designation', placeholder='Eg. Junior Design Engineer'),
                    Field('profile_name', placeholder='Eg. SDE, Management'),
                    'num_openings',
                    HTML("""
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Requirements',
                    # 'cpi_shortlist',
                    # 'minimum_cpi',
                    # 'percentage_x',
                    # 'percentage_xii',
                    # Field('percentage_x', css_class='col-md-6'),
                    # Field('percentage_xii', css_class='col-md-6'),
                    HTML('<h4>CPI</h4>'),
                    Div(
                        # Div('cpi_shortlist', css_class='col-md-12'),
                        # Div('minimum_cpi', css_class='col-md-12'),
                        Field('cpi_shortlist'),
                        Field('minimum_cpi'),
                        css_class='col-md-12'
                    ),

                    HTML('<h4>Percentage</h4>'),
                    Div(
                        # Div('percentage_x', css_class='col-md-12'),
                        # Div('percentage_xii', css_class='col-md-12'),
                        Field('percentage_x'),
                        Field('percentage_xii'),
                        css_class='col-md-12'
                    ),

                    'other_requirements',
                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Salary/Incentives',
                    # MultiField(
                    #     'B.Tech',
                    #     'ctc_btech',
                    #     'gross_btech',
                    # ),
                    'currency',
                    'ctc_btech',
                    'ctc_mtech',
                    'ctc_phd',
                    'ctc_msc',
                    'ctc_ma',
                    'gross_btech',
                    'gross_mtech',
                    'gross_phd',
                    'gross_msc',
                    'gross_ma',
                    'take_home_during_training',
                    'take_home_after_training',
                    'bonus',
                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Bond',
                    'bond',
                    Field('bond_link', placeholder='Leave empty if no bond is needed'),
                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <input type="submit" class="btn btn-success" value="Add Job" >
                    """)
                )
            )
        )


class AdminJobEditForm(ModelForm):
    opening_date = forms.DateInput(format=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Job
        exclude = ['alum_owner', 'company_owner', 'posted_by_alumnus', 'posted_by_company',
                   'posted_on', 'approved_on', 'last_updated']
        widgets = {
            'opening_date': DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False}),
            'application_deadline': DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False})
        }

    def __init__(self, *args, **kwargs):
        super(AdminJobEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Basic Information',
                    'description', 'designation', 'profile_name', 'num_openings',
                    HTML("""
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Requirements',
                    'cpi_shortlist', 'minimum_cpi', 'percentage_x',
                    'percentage_xii', 'other_requirements',
                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Salary/Incentives',

                    'currency', 'ctc_btech', 'ctc_mtech', 'ctc_phd', 'ctc_msc', 'ctc_ma',
                    'gross_btech', 'gross_mtech', 'gross_phd', 'gross_msc', 'gross_ma',
                    'take_home_during_training', 'take_home_after_training', 'bonus',

                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Bond',

                    'bond', 'bond_link',

                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Settings',

                    'opening_date', 'application_deadline', 'approved',

                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <input type="submit" class="btn btn-primary" value="Save" >
                    """)
                )
            )
        )


class CompanyEventForm(forms.Form):

    class Meta:
        model = Event
        fields = ['title', 'event_type', 'event_date', 'event_type']


class CompanyProfileEdit(ModelForm):
    company_name = forms.CharField(max_length=30,
                                   label="Company Name",
                                   widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Company
        exclude = ['user', 'password_copy', 'approved']

    def __init__(self, *args, **kwargs):
        super(CompanyProfileEdit, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'General Details',

                    'company_name', 'description', 'postal_address',
                    'website', 'organization_type', 'industry_sector'
                ),
                Tab(
                    'HR Details',

                    'head_hr_name', 'head_hr_email', 'head_hr_designation', 'head_hr_mobile',
                    'head_hr_fax',
                    'first_hr_name', 'first_hr_email', 'first_hr_designation', 'first_hr_mobile',
                    'first_hr_fax'
                )
            )
        )


class StudentSearchForm(forms.Form):

    year = forms.DecimalField(max_digits=4, decimal_places=0, required=True)
    dept_code = forms.CharField(max_length=4, required=True, label='Department Code')
    programme = forms.ChoiceField(choices=PROGRAMMES, required=True)
    minor_status = forms.BooleanField(initial=False, required=False)


class AddStudent(ModelForm):
    # Login Credentials
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = Student
        exclude = ['user', 'placed', 'cv1', 'cv2', 'intern2', 'intern3', 'ppo']
        widgets = {
            'gap_reason': forms.Textarea(attrs=dict(rows=4, cols=15))
        }


class AddCompany(ModelForm):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=30)

    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddCompany, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Login Credentials',
                    'username',
                    'password'
                ),
                Tab(
                    'General Details',
                    'company_name',
                    'description',
                    'postal_address',
                    'website',
                    'organization_type',
                    'industry_sector'
                ),
                Tab(
                    'HR Details',
                    'head_hr_name',
                    'head_hr_email',
                    'head_hr_designation',
                    'head_hr_mobile',
                    'head_hr_fax',
                    'first_hr_name',
                    'first_hr_email',
                    'first_hr_designation',
                    'first_hr_mobile',
                    'first_hr_fax'
                )
            )
        )


class EditCompany(ModelForm):

    class Meta:
        model = Company
        exclude = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(EditCompany, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'General Details',
                    'company_name',
                    'description',
                    'postal_address',
                    'website',
                    'organization_type',
                    'industry_sector'
                ),
                Tab(
                    'HR Details',
                    'head_hr_name',
                    'head_hr_email',
                    'head_hr_designation',
                    'head_hr_mobile',
                    'head_hr_fax',
                    'first_hr_name',
                    'first_hr_email',
                    'first_hr_designation',
                    'first_hr_mobile',
                    'first_hr_fax'
                ),
                Tab(
                    'Settings',
                    'approved',
                )
            )
        )


class EditStudentAdmin(ModelForm):

    class Meta:
        model = Student
        exclude = ['username', 'password']


class SelectCVForm(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop("extra")
        super(SelectCVForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(extra):
            self.fields['custom_%s' % i] = forms.BooleanField(label=question, initial=True, required=False)

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)

    def clean(self):
        all_false = True
        for (question, answer) in self.extra_answers():
            if answer is True:
                all_false = False
        if all_false:
            raise ValidationError("At least one CV must be selected.")


class AlumniProfileForm(ModelForm):
    class Meta:
        model = Alumni
        exclude = ['user', 'cv']


class AlumCVUpload(ModelForm):
    class Meta:
        model = Alumni
        fields = ['cv']


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        exclude = ['stud']


class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        exclude = ['stud']


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['cv1', 'cv2']

    def clean(self):
        cleaned_data = super(CVForm, self).clean()
        if not bool(cleaned_data['cv1']) and not bool(cleaned_data['cv2']):
            raise ValidationError("Provide at least one file.", code='invalid')


class CompanySignup(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['company_name', 'description', 'postal_address', 'website', 'organization_type',
                  'industry_sector', 'head_hr_name', 'head_hr_email', 'head_hr_designation',
                  'head_hr_mobile', 'head_hr_fax']


class UserProfileForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput,
                                help_text="Enter the same password as before, for verification.")

    class Meta:
        model = UserProfile
        fields = ['username']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        return password2

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password1']
        user = UserProfile.objects.create_user(username=username, password=password)
        return user


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(CustomPasswordChangeForm, self).__init__(request.user, *args, **kwargs)


class CompanyJobRelForm(forms.ModelForm):
    class Meta:
        model = StudentJobRelation
        fields = ['shortlist_init', 'shortlist_approved', 'placed_init', 'placed_approved']

    def __init__(self, *args, **kwargs):
        super(CompanyJobRelForm, self).__init__(*args, **kwargs)
        self.fields['shortlist_approved'].disabled = True
        self.fields['placed_approved'].disabled = True
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            if instance.shortlist_init is True:
                if instance.shortlist_approved is None:
                    self.fields['placed_init'].disabled = True
                elif instance.shortlist_approved is True:
                    self.fields['shortlist_init'].disabled = True
                elif instance.shortlist_approved is False:
                    self.fields['shortlist_init'].disabled = True
                    self.fields['placed_init'].disabled = True
            else:
                self.fields['placed_init'].disabled = True
            if instance.placed_init is True:
                self.fields['shortlist_init'].disabled = True
                if instance.placed_approved is not None:
                    self.fields['placed_init'].disabled = True


class AdminJobRelForm(forms.ModelForm):
    class Meta:
        model = StudentJobRelation
        fields = ['shortlist_init', 'shortlist_approved', 'placed_init', 'placed_approved']

    def __init__(self, *args, **kwargs):
        super(AdminJobRelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['shortlist_init'].disabled = True
        self.fields['placed_init'].disabled = True
        if instance and instance.pk:
            if instance.placed_init is True:
                self.fields['shortlist_approved'].disabled = True


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'event_type', 'event_date', 'event_time']
        widgets = {
            'event_date': DateTimePicker(options={'format': 'YYYY-MM-DD', 'pickTime': False}),
            'event_time': DateTimePicker(options={'format': 'hh mm A', "pickSeconds": False, 'stepping': 30}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = '__all__'
        widgets = {
            'open_for_placement': CheckBoxBootstrapSwitch(
                switch={'size': 'large', 'on': 'warning', 'text-label': 'Switch Me'}
            )
        }
