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


class LoginForm(forms.Form):
    """
    Common Login Form for all Users.
    """
    username = forms.CharField(required=True, label='Webmail', max_length=25)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class EditStudProfileForm(ModelForm):

    class Meta:
        model = Student
        fields = ['roll_no', 'name', 'dob',
                  'sex', 'category', 'nationality', 'minor_year',
                  'minor_dept', 'minor_prog', 'year', 'dept', 'prog',
                  'hostel', 'room_no', 'iitg_webmail', 'alternative_email',
                  'mobile_campus', 'mobile_campus_alternative',
                  'mobile_home', 'address_line1', 'address_line2',
                  'address_line3', 'pin_code', 'percentage_x',
                  'percentage_xii', 'board_x', 'board_xii', 'medium_x',
                  'medium_xii', 'passing_year_x', 'passing_year_xii',
                  'gap_in_study', 'gap_reason', 'jee_air_rank',
                  'linkedin_link', 'cpi', 'spi_1_sem', 'spi_2_sem',
                  'spi_3_sem', 'spi_4_sem', 'spi_5_sem', 'spi_6_sem',
                  'active_backlogs']

        widgets = {
            'gap_reason': forms.Textarea(attrs={'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super(EditStudProfileForm, self).__init__(*args, **kwargs)
        self.fields['roll_no'].disabled = True
        self.fields['iitg_webmail'].disabled = True
        self.fields['name'].disabled = True
        self.fields['year'].disabled = True
        self.fields['dept'].disabled = True
        self.fields['prog'].disabled = True
        self.fields['minor_year'].disabled = True
        self.fields['minor_dept'].disabled = True
        self.fields['minor_prog'].disabled = True
        self.fields['jee_air_rank'].label = 'JEE AIR Rank'
        self.fields['percentage_x'].label = 'Percentage X'
        self.fields['percentage_xii'].label = 'Percentage XII'
        self.fields['board_x'].label = 'X Examination Board'
        self.fields['board_xii'].label = 'XII Examination Board'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Student Information',

                    'roll_no',
                    'iitg_webmail',
                    'name',
                    'dob',
                    'sex',
                    'category',
                    'nationality',
                    'year',
                    'dept',
                    'prog',
                    'minor_year',
                    'minor_dept',
                    'minor_prog',
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
                    'active_backlogs',
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

        return cleaned_data


class CompanyJobForm(ModelForm):
    """
    Job ModelForm for Company Users to create Job instances.
    """
    class Meta:
        model = Job
        fields = ['description', 'designation', 'profile_name',
                  'cpi_shortlist', 'minimum_cpi', 'percentage_x',
                  'percentage_xii', 'num_openings', 'currency', 'ctc_btech',
                  'ctc_mtech', 'ctc_msc', 'ctc_ma', 'ctc_phd', 'gross_btech',
                  'gross_mtech', 'gross_ma', 'gross_msc', 'gross_phd',
                  'bond_link']

    def clean(self):
        cleaned_data = super(CompanyJobForm, self).clean()
        ctc_btech = cleaned_data['ctc_btech']
        gross_btech = cleaned_data['gross_btech']
        ctc_mtech = cleaned_data['ctc_mtech']
        gross_mtech = cleaned_data['gross_mtech']
        ctc_msc = cleaned_data['ctc_msc']
        gross_msc = cleaned_data['gross_msc']
        ctc_ma = cleaned_data['ctc_ma']
        gross_ma = cleaned_data['gross_ma']
        ctc_phd = cleaned_data['ctc_phd']
        gross_phd = cleaned_data['gross_phd']
        if ctc_btech < gross_btech:
            raise ValidationError("Error: In Salary section, Gross B.Tech. "
                                  "cannot be greater than CTC B.Tech.")
        elif ctc_mtech < gross_mtech:
            raise ValidationError("Error: In Salary section, Gross M.Tech. "
                                  "cannot be greater than CTC M.Tech.")
        elif ctc_msc < gross_msc:
            raise ValidationError("Error: In Salary section, Gross M.Sc. "
                                  "cannot be greater than CTC M.Sc")
        elif ctc_ma < gross_ma:
            raise ValidationError("Error: In Salary section, Gross M.A. "
                                  "cannot be greater than CTC M.A.")
        elif ctc_phd < gross_phd:
            raise ValidationError("Error: In Salary section, Gross Ph.D. "
                                  "cannot be greater than CTC Ph.D.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(CompanyJobForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['bond_link'].help_text = 'Upload the bond document.'
        self.fields['cpi_shortlist'].help_text = 'Select if CPI-based ' \
                                                 'filtering is needed.'

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Basic Information',
                    Field('description'),
                    Field('designation', placeholder='Eg. Software Engineer'),
                    Field('profile_name', placeholder='Eg. SDE, Management'),
                    'num_openings',
                    HTML("""
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Requirements',
                    HTML('<h4>CPI</h4>'),
                    Div(
                        Field('cpi_shortlist'),
                        Field('minimum_cpi'),
                        css_class='col-md-12'
                    ),

                    HTML('<h4>Percentage</h4>'),
                    Div(
                        Field('percentage_x'),
                        Field('percentage_xii'),
                        css_class='col-md-12'
                    ),
                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Salary Breakdown',

                    'currency',
                    HTML('<h4>B.Tech</h4>'),
                    Div(
                        Field('ctc_btech'),
                        Field('gross_btech'),
                        css_class='col-md-12'
                    ),
                    HTML('<h4>M.Tech</h4>'),
                    Div(
                        Field('ctc_mtech'),
                        Field('gross_mtech'),
                        css_class='col-md-12'
                    ),
                    HTML('<h4>Ph.D.</h4>'),
                    Div(
                        Field('ctc_phd'),
                        Field('gross_phd'),
                        css_class='col-md-12'
                    ),
                    HTML('<h4>M.Sc.</h4>'),
                    Div(
                        Field('ctc_msc'),
                        Field('gross_msc'),
                        css_class='col-md-12'
                    ),
                    HTML('<h4>M.A.</h4>'),
                    Div(
                        Field('ctc_ma'),
                        Field('gross_ma'),
                        css_class='col-md-12'
                    ),
                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Bond',
                    # 'bond',
                    Field('bond_link',
                          placeholder='Leave empty if no bond is needed'),
                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <input type="submit" class="btn btn-success"
                        value="Add Job" >
                    """)
                )
            )
        )


class AdminJobEditForm(ModelForm):
    """
    Job ModelForm for Admin Users to create Job instances.
    """
    class Meta:
        model = Job
        fields = ['description', 'designation', 'profile_name',
                  'cpi_shortlist', 'minimum_cpi', 'percentage_x',
                  'percentage_xii', 'num_openings', 'currency', 'ctc_btech',
                  'ctc_mtech', 'ctc_msc', 'ctc_ma', 'ctc_phd', 'gross_btech',
                  'gross_mtech', 'gross_ma', 'gross_msc', 'gross_phd',
                  'bond_link', 'opening_date', 'application_deadline',
                  'backlog_filter', 'num_backlogs_allowed']
        widgets = {
            'opening_date': DateTimePicker(options={'format': 'YYYY-MM-DD',
                                                    'pickTime': False}),
            'application_deadline': DateTimePicker(options={
                'format': 'YYYY-MM-DD', 'pickTime': False})
        }

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

                    'backlog_filter',
                    'num_backlogs_allowed',
                    'cpi_shortlist',
                    'minimum_cpi',
                    'percentage_x',
                    'percentage_xii',
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

                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Bond',

                    'bond_link',

                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <a class="btn btn-primary btnNext" >Next</a>
                    """)
                ),
                Tab(
                    'Settings',

                    'opening_date', 'application_deadline',

                    HTML("""
                        <a class="btn btn-primary btnPrevious" >Previous</a>
                        <input type="submit" class="btn btn-primary"
                        value="Save" >
                    """)
                )
            )
        )


class CompanyEventForm(forms.Form):

    class Meta:
        model = Event
        fields = ['title', 'event_type', 'event_date1', 'event_date2']


class CompanyProfileEdit(ModelForm):
    """
    Company ModelForm for Company Users to update Company instance.
    """

    class Meta:
        model = Company
        fields = ['company_name', 'description', 'postal_address', 'website',
                  'organization_type', 'office_contact_no',
                  'industry_sector', 'head_hr_name', 'head_hr_email',
                  'head_hr_designation', 'head_hr_mobile', 'head_hr_fax',
                  'first_hr_name', 'first_hr_email', 'first_hr_designation',
                  'first_hr_mobile', 'first_hr_fax']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'postal_address': forms.Textarea(attrs={'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super(CompanyProfileEdit, self).__init__(*args, **kwargs)
        self.fields['company_name'].disabled = True
        self.fields['postal_address'].disabled = True
        self.fields['website'].disabled = True
        self.fields['organization_type'].disabled = True
        self.fields['industry_sector'].disabled = True
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
                    'industry_sector',
                    'office_contact_no'
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


class StudentSearchForm(forms.Form):
    # TODO: Update this as per 10/8/16 README
    name = forms.CharField(max_length=100, required=False,
                           label='Full Name (or part of name)')
    username = forms.CharField(max_length=50, label='Username', required=False)
    roll_no = forms.IntegerField(label='Roll Number', required=False)

    def clean(self):
        cleaned_data = super(StudentSearchForm, self).clean()
        username = cleaned_data['username']
        roll_no = cleaned_data['roll_no']
        name = cleaned_data['name']

        if username is None and roll_no is None and name is None:
            raise ValidationError("All fields cannot be empty")
        if roll_no is not None:
            try:
                int(roll_no)
            except ValueError:
                raise ValidationError("Roll Number must be a number")
        return cleaned_data


class AddCompany(ModelForm):
    """
    Company ModelForm (with username and password fields for related
    UserProfile) for Admin Users to create Company instances.
    """
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=30)

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'postal_address': forms.Textarea(attrs={'rows': 4})
        }

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
    """
    Company ModelForm for Admin Users to update Company instances.
    """
    class Meta:
        model = Company
        fields = ['company_name', 'description', 'postal_address', 'website',
                  'organization_type', 'industry_sector', 'head_hr_name',
                  'head_hr_email', 'head_hr_designation', 'head_hr_mobile',
                  'head_hr_fax', 'first_hr_name', 'first_hr_email',
                  'first_hr_designation', 'first_hr_mobile', 'first_hr_fax',
                  'approved']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'postal_address': forms.Textarea(attrs={'rows': 4})
        }

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
                    'industry_sector',
                    'office_contact_no'
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
    """
    Student ModelForm for Admin Users to update Student instances.
    """

    class Meta:
        model = Student
        exclude = ['username', 'password']


class SelectCVForm(forms.Form):
    """
    CV ModelForm for Student Users to create and update CVs.
    """
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop("extra")
        super(SelectCVForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(extra):
            self.fields['custom_%s' % i] = forms.BooleanField(label=question,
                                                              initial=True,
                                                              required=False)

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)

    def clean(self):
        all_false = True
        all_true = True
        for (question, answer) in self.extra_answers():
            if answer is True:
                all_false = False
            if answer is False:
                all_true = False
        if all_false:
            raise ValidationError("One CV must be selected.")
        if all_true:
            raise ValidationError("Only one CV must be selected.")


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
                raise ValidationError("Provide at least one file.",
                                      code='invalid')
            return cleaned_data


class CompanySignup(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['company_name', 'description', 'postal_address', 'website', 'organization_type',
                  'industry_sector', 'office_contact_no', 'head_hr_name',
                  'head_hr_email', 'head_hr_designation',
                  'head_hr_mobile', 'head_hr_fax']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'postal_address': forms.Textarea(attrs={'rows': 4})
        }


class UserProfileForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password "
                                          "as before, for verification.")

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
        user = UserProfile.objects.create_user(username=username,
                                               password=password)
        return user


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(CustomPasswordChangeForm, self).__init__(request.user, *args,
                                                       **kwargs)


class CompanyJobRelForm(forms.ModelForm):
    class Meta:
        model = StudentJobRelation
        fields = ['shortlist_init', 'placed_init',
                  'placed_approved']

    def __init__(self, *args, **kwargs):
        super(CompanyJobRelForm, self).__init__(*args, **kwargs)
        self.fields['shortlist_approved'].disabled = True
        self.fields['placed_approved'].disabled = True
        instance = getattr(self, 'instance', None)

        # disable fields based on what approvals are pending
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

    def save(self, commit=True):
        instance = super(CompanyJobRelForm, self).save(commit=False)
        # unset dropped value only if
        # 1. current value of 'dropped' is True
        # 2. form has changed, i.e. recruiter has tried to reshortlist student

        if self.has_changed() and instance.dropped is True:
            # Optimized version of above code can be this
            # Instead of checking all fields, only check the
            # shortlist_init field
            # self.fields['shortlist_init].has_changed()
            instance.dropped = False
        # save the changes
        if commit:
            instance.save()
        return instance


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        # is_approved Field has been included in fields but this field will
        # not be rendered in the form because of HiddenField() widget.
        # Then why include this field at all?
        # It has been included to verify if an event has been already
        # approved by admin. If approved, Company should not be able to
        # edit/update the event using corresponding UpdateView()
        fields = ['title', 'event_type', 'duration', 'logistics', 'remark',
                  'is_approved']

        widgets = {
                    'logistics': forms.Textarea(attrs={'rows': 4}),
                    'remark': forms.Textarea(attrs={'rows': 4}),
                    'is_approved': forms.HiddenInput()
                }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class AdminEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'event_type', 'duration', 'logistics', 'remark',
                  'is_approved', 'final_date']
        widgets = {
            'final_date': DateTimePicker(options={'format': 'YYYY-MM-DD',
                                                  'pickTime': False}),
            'logistics': forms.Textarea(attrs={'rows': 4}),
            'remark': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(AdminEventForm, self).__init__(*args, **kwargs)
        self.fields['title'].disabled = True
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean(self):
        cleaned_data = super(AdminEventForm, self).clean()
        is_approved = cleaned_data.get('is_approved')
        final_date = cleaned_data.get('final_date')

        if is_approved is None and final_date is None:
            return cleaned_data
        elif is_approved is not None and final_date is not None:
            return cleaned_data
        else:
            err_msg = "Either update both 'Approval Status' and " \
                      "'Approved Date' or leave both unupdated."
            raise forms.ValidationError(err_msg)


class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = '__all__'
        widgets = {
            'open_for_placement': CheckBoxBootstrapSwitch(
                switch={'size': 'large', 'on': 'warning',
                        'text-label': 'Switch Me'}
            )
        }


class StudentProfileUploadForm(forms.Form):

    csv = forms.FileField(required=False, allow_empty_file=True,
                          label='Upload CSV')


class StudentFeeCSVForm(forms.Form):

    csv = forms.FileField(required=False, allow_empty_file=True,
                          label='Upload CSV')
