# TODO: Replace forms.Form with ModelForm wherever possible
# TODO: Add CSS classes to form inputs (Naveen)
# (http://stackoverflow.com/questions/401025/define-css-class-in-django-forms)

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, inlineformset_factory
from functools import partial
# Project imports
from models import *
from constants import *
# Crispy Widget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
# Captcha
from captcha.fields import ReCaptchaField


# Date Widget
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

JobProgFormSet = inlineformset_factory(Job, ProgrammeJobRelation, fields=('year', 'dept', 'prog'), extra=10)


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Webmail', max_length=25)
    password = forms.CharField(required=True, widget=forms.PasswordInput, label="Password")
    captcha = ReCaptchaField()


class EditStudProfileForm(ModelForm):

    class Meta:
        model = Student
        exclude = ['user', 'avatar', 'signature', 'cv1', 'cv2', 'placed', 'inter2', 'intern3', 'ppo']

    def __init__(self, *args, **kwargs):
        super(EditStudProfileForm, self).__init__(*args, **kwargs)
        # TODO: Un-comment this in production
        # instance = getattr(self, 'instance', None)
        # if instance and instance.pk:
        #     self.fields['year'].required = False
        #     self.fields['year'].widget.attrs['disabled'] = 'disabled'
        #     self.fields['dept'].required = False
        #     self.fields['dept'].widget.attrs['disabled'] = 'disabled'
        #     self.fields['prog'].required = False
        #     self.fields['prog'].widget.attrs['disabled'] = 'disabled'
        self.helper = FormHelper()
        self.helper.form_tag = False
        # TODO: See inheriting layouts
        # TODO: http://django-crispy-forms.readthedocs.org/en/d-0/layouts.html#inheriting-layouts
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Student Information',
                    'roll_no',
                    AppendedText('iitg_webmail', '@iitg.ernet.in'),
                    'first_name',
                    'middle_name',
                    'last_name',
                    'dob',
                    'sex',
                    'category',
                    'nationality',
                    'year',
                    'dept',
                    'prog',
                    'minor_programme',
                    'hostel',
                    'room_no'
                ),
                Tab(
                    'Contact Information',
                    PrependedText('linkedin_link', 'https://'),
                    'alternative_email',
                    'mobile_campus',
                    'mobile_campus_alternative',
                    'mobile_home'
                ),
                Tab(
                    'Home Address',
                    'address_line1',
                    'address_line2',
                    'address_line3',
                    'pin_code'
                ),
                Tab(
                    'Academic',
                    'jee_air_rank',
                    'percentage_x',
                    'percentage_xii',
                    'board_x',
                    'board_xii',
                    'medium_x',
                    'medium_xii',
                    'passing_year_x',
                    'passing_year_xii',
                    'gap_in_study',
                    'gap_reason',
                ),
                Tab(
                    'CPI',
                    'cpi',
                    'spi_1_sem',
                    'spi_2_sem',
                    'spi_3_sem',
                    'spi_4_sem',
                    'spi_5_sem',
                    'spi_6_sem',
                )
            )
        )

    # TODO: Updated in Django 1.9
    # TODO: https://docs.djangoproject.com/en/1.9/ref/forms/fields/#disabled
    # TODO: Un-comment this in production
    # def clean_year(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         return instance.year
    #     else:
    #         return self.cleaned_data['year']
    #
    # def clean_dept(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         return instance.dept
    #     else:
    #         return self.cleaned_data['dept']
    #
    # def clean_prog(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         return instance.prog
    #     else:
    #         return self.cleaned_data['prog']


class AlumLoginForm(forms.Form):
    username = forms.CharField(required=True, label='Webmail', max_length=25)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    # captcha = CaptchaField()


class JobEditForm(ModelForm):
    class Meta:
        model = Job
        exclude = ['alum_owner', 'company_owner', 'posted_by_alumnus', 'posted_by_company',
                   'posted_on', 'approved', 'approved_on', 'sent_back', 'last_updated', 'opening_date',
                   'application_deadline']

    def __init__(self, *args, **kwargs):
        """
        Init function.
        Form layout is defined here.
        :param args: args
        :param kwargs:kwargs
        :return:void
        """
        super(JobEditForm, self).__init__(*args, **kwargs)
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
    class Meta:
        model = Job
        exclude = ['alum_owner', 'company_owner', 'posted_by_alumnus', 'posted_by_company',
                   'posted_on', 'approved_on', 'last_updated']

    def __init__(self, *args, **kwargs):
        super(AdminJobEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Basic Information',
                    'description',
                    'designation',
                    'profile_name',
                    'num_openings',
                    HTML("""
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Requirements',
                    'cpi_shortlist',
                    'minimum_cpi',
                    'percentage_x',
                    'percentage_xii',
                    'other_requirements',
                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Salary/Incentives',
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
                    'bond_link',
                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Settings',
                    'opening_date',
                    'application_deadline',
                    'approved',
                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <input type="submit" class="btn btn-primary" value="Save" >
                    """)
                )
            )
        )


class RequestEventForm(forms.Form):
    title = forms.CharField(max_length=30, required=True, label='Event Title')
    date1 = forms.DateField(label='Date priority 1', required=True, widget=DateInput())
    date2 = forms.DateField(label='Date priority 2', required=True, widget=DateInput())
    date3 = forms.DateField(label='Date priority 3', required=True, widget=DateInput())


class CompanySignupForm(ModelForm):

    # Captcha Field
    # captcha = CaptchaField()

    class Meta:
        model = CompanyReg
        exclude = []

    def __init__(self, *args, **kwargs):
        super(CompanySignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'General Details',
                    'company_name_reg',
                    'description_reg',
                    'postal_address_reg',
                    'website_reg',
                    'organization_type_reg',
                    'industry_sector_reg',
                    # 'captcha',
                    HTML("""
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'HR Details',
                    'head_hr_name_reg',
                    'head_hr_email_reg',
                    'head_hr_designation_reg',
                    'head_hr_mobile_reg',
                    'head_hr_fax_reg',
                    'first_hr_name_reg',
                    'first_hr_email_reg',
                    'first_hr_designation_reg',
                    'first_hr_mobile_reg',
                    'first_hr_fax_reg',
                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <input type="submit" class="btn btn-primary" value="Sign Up" >
                    """)
                )
            )
        )


class CompanyProfileEdit(ModelForm):
    company_name = forms.CharField(max_length=30,
                                   label="Company Name",
                                   widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Company
        exclude = ['user', 'password_copy', 'approved', 'sent_back']

    def __init__(self, *args, **kwargs):
        super(CompanyProfileEdit, self).__init__(*args, **kwargs)
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
                )
            )
        )


# Search forms
class StudentSearchForm(forms.Form):
    programme = forms.ChoiceField(label="Programme", required=True, choices=PROGRAMMES)
    year = forms.DecimalField(required=True)
    department = forms.ChoiceField(label="Department", required=True, choices=DEPARTMENTS)


# Admin User Management forms
class AddStudent(ModelForm):
    # Login Credentials
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = Student
        exclude = ['user', 'avatar', 'signature', 'placed', 'cv1', 'cv2', 'intern2', 'intern3', 'ppo']


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
                    'sent_back'
                )
            )
        )


class EditStudentAdmin(ModelForm):

    class Meta:
        model = Student
        exclude = ['username', 'password', 'avatar', 'signature']


class AddEditDepartment(ModelForm):
    class Meta:
        model = Department
        fields = "__all__"


class AddEditProgramme(ModelForm):
    class Meta:
        model = Programme
        fields = "__all__"


class AddEditYear(ModelForm):
    class Meta:
        model = Year
        fields = "__all__"


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


class StudCVForm(forms.Form):
    cv1 = forms.FileField(label='CV1', required=False, max_length=100)
    cv2 = forms.FileField(label='CV2', required=False, max_length=100)

    def __init__(self, *args, **kwargs):
        super(StudCVForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout()

    def clean(self):
        form_data = self.cleaned_data
        if not bool(form_data['cv1']) and not bool(form_data['cv2']):
            raise ValidationError("Provide at least one file.")


class AvatarSignForm(ModelForm):
    class Meta:
        model = Student
        fields = ['avatar', 'signature']


class AlumniProfileForm(ModelForm):
    class Meta:
        model = Alumni
        exclude = ['user', 'cv']


class AlumCVUpload(ModelForm):
    class Meta:
        model = Alumni
        fields = ['cv']
