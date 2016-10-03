from django import forms
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm
from django.template.defaultfilters import filesizeformat

from material import *

from models import *


class LoginForm(forms.Form):
    """
    Common Login Form for all Users.
    """
    username = forms.CharField(required=True, label='Username', max_length=50)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, initial=False,
                                     label='Remember Me')


class EditStudProfileForm(ModelForm):

    layout = Layout(
        Fieldset(
            'Basic Information',
            Row('dob'),
            Row('hostel', 'room_no'),
            Row('mobile_campus'),
            Row('mobile_campus_alternative'),
            Row('mobile_home'),
            Row('alternative_email'),
            Row('linkedin_link'),
            Row('pd_status'),
        ),
        Fieldset(
            'Permanent Address',
            'address_line1', 'address_line2', 'address_line3', 'pin_code'
        ),
        Fieldset(
            'Academic Performance',
            Row(
                Column('percentage_x', 'board_x', 'passing_year_x',
                       'medium_x'),
                Column('percentage_xii', 'board_xii', 'passing_year_xii',
                       'medium_xii'),
            ),
            Row('gap_in_study'),
            Row('gap_reason'),
            Row('jee_air_rank', 'rank_category'),
        ),
        Fieldset(
            'IITG Academic Performance',
            Row('spi_1_sem', 'spi_2_sem', 'spi_3_sem'),
            Row('spi_4_sem', 'spi_5_sem', 'spi_6_sem'),
            Row('active_backlogs')
        )
    )

    class Meta:
        model = Student
        fields = ['dob','hostel', 'room_no','alternative_email',
                  'mobile_campus', 'mobile_campus_alternative',
                  'mobile_home', 'address_line1', 'address_line2',
                  'address_line3', 'pin_code', 'percentage_x',
                  'percentage_xii', 'board_x', 'board_xii', 'medium_x',
                  'medium_xii', 'passing_year_x', 'passing_year_xii',
                  'gap_in_study', 'gap_reason', 'jee_air_rank',
                  'linkedin_link', 'spi_1_sem', 'spi_2_sem',
                  'spi_3_sem', 'spi_4_sem', 'spi_5_sem', 'spi_6_sem',
                  'active_backlogs', 'rank_category', 'pd_status']

        widgets = {
            'gap_reason': forms.Textarea(attrs={'rows': 4}),
        }


class CompanyJobForm(ModelForm):
    """
    Job ModelForm for Company Users to create Job instances.
    """

    layout = Layout(
        Fieldset('Basic Information',
                 'designation', 'profile_name', 'description', 'num_openings'),
        Fieldset('CPI and Percentage Requirements',
                 Row(
                     Column('cpi_shortlist', 'minimum_cpi', span_columns=6),
                     Column('percentage_x', 'percentage_xii', span_columns=6),
                 )
                 ),
        Fieldset('Salary Breakdown (Only fill details for programmes your '
                 'firm will be hiring)',
                 'currency',
                 Row('ctc_btech', 'gross_btech'),
                 Row('ctc_mtech', 'gross_mtech'),
                 Row('ctc_msc', 'gross_msc'),
                 Row('ctc_ma', 'gross_ma'),
                 Row('ctc_phd', 'gross_phd'),
                 Row('ctc_msr', 'gross_msr'),
                 Row('additional_info')
                 ),
        Fieldset('Legal Document', 'bond_link')
    )

    class Meta:
        model = Job
        fields = ['description', 'designation', 'profile_name',
                  'cpi_shortlist', 'minimum_cpi', 'percentage_x',
                  'percentage_xii', 'num_openings', 'currency', 'ctc_btech',
                  'ctc_mtech', 'ctc_msc', 'ctc_ma', 'ctc_phd', 'gross_btech',
                  'gross_mtech', 'gross_ma', 'gross_msc', 'gross_phd',
                  'bond_link', 'additional_info', 'ctc_msr', 'gross_msr']

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
        ctc_msr = cleaned_data['ctc_msr']
        gross_msr = cleaned_data['gross_msr']

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
        elif ctc_msr < gross_msr:
            raise ValidationError("Error: In Salary section, Gross MS(R) "
                                  "cannot be greater than CTC MS(R).")

        cpi_shortlist = cleaned_data['cpi_shortlist']
        minimum_cpi = cleaned_data['minimum_cpi']

        if cpi_shortlist is True:
            if minimum_cpi is None:
                error = 'Minimum CPI field cannot be left blank if CPI ' \
                        'Shortlist option in checked.'
                raise ValidationError(error)
        else:
            cleaned_data['minimim_cpi'] = 4.0
        if minimum_cpi is None:
            cleaned_data['minimim_cpi'] = 4.0
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(CompanyJobForm, self).__init__(*args, **kwargs)


class AdminJobEditForm(ModelForm):
    """
    Job ModelForm for Admin Users to create Job instances.
    """

    layout = Layout(
        Fieldset('Basic Information',
                 'designation', 'profile_name', 'description', 'num_openings'),
        Fieldset('CPI and Percentage Requirements',
                 Row(
                     Column('cpi_shortlist', 'minimum_cpi', span_columns=4),
                     Column('percentage_x', 'percentage_xii', span_columns=4),
                     Column('backlog_filter', 'num_backlogs_allowed',
                            span_columns=4),
                 )
                 # Row('percentage_x', 'percentage_xii'),
                 # Row('percentage_x','percentage_xii')
                 ),
        Fieldset('Salary Breakdown (Only fill details for programmes your '
                 'firm will be hiring)',
                 'currency',
                 Row('ctc_btech', 'gross_btech'),
                 Row('ctc_mtech', 'gross_mtech'),
                 Row('ctc_msc', 'gross_msc'),
                 Row('ctc_ma', 'gross_ma'),
                 Row('ctc_phd', 'gross_phd'),
                 Row('ctc_msr', 'gross_msr'),
                 Row('additional_info')
                 ),
        Fieldset('Legal Document', 'bond_link'),
        Fieldset(
            'Opening and Closing Dates',
            'opening_datetime',
            'application_deadline',
        )
    )

    class Meta:
        model = Job
        fields = ['description', 'designation', 'profile_name',
                  'cpi_shortlist', 'minimum_cpi', 'percentage_x',
                  'percentage_xii', 'num_openings', 'currency', 'ctc_btech',
                  'ctc_mtech', 'ctc_msc', 'ctc_ma', 'ctc_phd', 'gross_btech',
                  'gross_mtech', 'gross_ma', 'gross_msc', 'gross_phd',
                  'bond_link', 'opening_datetime', 'application_deadline',
                  'backlog_filter', 'num_backlogs_allowed', 'additional_info',
                  'ctc_msr', 'gross_msr']

    def __init__(self, *args, **kwargs):
        super(AdminJobEditForm, self).__init__(*args, **kwargs)
        self.fields['designation'].widget.attrs['readonly'] = True
        self.fields['profile_name'].widget.attrs['readonly'] = True


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

    layout = Layout(
        Fieldset('Company Details',
                 'company_name', 'description', 'postal_address',
                 'website', 'office_contact_no',
                 Row(Span6('organization_type'), Span6('industry_sector'))),
        Fieldset('Head HR (First Point of Contact)',
                 'head_hr_name', 'head_hr_email', 'head_hr_mobile',
                 'head_hr_designation', 'head_hr_fax'),
        Fieldset('First HR (Second Point of Contact)',
                 'first_hr_name', 'first_hr_email', 'first_hr_mobile',
                 'first_hr_designation', 'first_hr_fax')
    )

    def __init__(self, *args, **kwargs):
        super(CompanyProfileEdit, self).__init__(*args, **kwargs)
        self.fields['company_name'].disabled = True
        self.fields['postal_address'].disabled = True
        self.fields['website'].disabled = True
        self.fields['organization_type'].disabled = True
        self.fields['industry_sector'].disabled = True


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


class EditCompany(ModelForm):
    """
    Company ModelForm for Admin Users to update Company instances.
    """

    layout = Layout(
        Fieldset('Company Details',
                 'company_name', 'description', 'postal_address',
                 'website', 'office_contact_no',
                 Row(Span6('organization_type'), Span6('industry_sector'))),
        Fieldset('First Point of Contact',
                 'head_hr_name', 'head_hr_email', 'head_hr_mobile',
                 'head_hr_designation', 'head_hr_fax'),
        Fieldset('Second Point of Contact',
                 'first_hr_name', 'first_hr_email', 'first_hr_mobile',
                 'first_hr_designation', 'first_hr_fax')
    )

    class Meta:
        model = Company
        fields = ['company_name', 'description', 'postal_address', 'website',
                  'organization_type', 'industry_sector', 'head_hr_name',
                  'head_hr_email', 'head_hr_designation', 'head_hr_mobile',
                  'head_hr_fax', 'first_hr_name', 'first_hr_email',
                  'first_hr_designation', 'first_hr_mobile', 'first_hr_fax',
                  'office_contact_no']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'postal_address': forms.Textarea(attrs={'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super(EditCompany, self).__init__(*args, **kwargs)


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
            self.fields['custom_%s' % i] = forms.BooleanField(
                label=str(question).upper(), initial=False, required=False)

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)

    def clean(self):
        true_count = 0
        false_count = 0
        for (question, answer) in self.extra_answers():
            if answer is True:
                true_count += 1
            if answer is False:
                false_count += 1
        if true_count is 0 and false_count is not 0:
            raise ValidationError("Select one CV.")
        if true_count is 2 and false_count is 0:
            raise ValidationError("Select only one CV.")
        return self.cleaned_data


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
        cv1 = self.cleaned_data.get('cv1', None)
        cv2 = self.cleaned_data.get('cv2', None)
        if not bool(cv1) and not bool(cv2):
            raise ValidationError("Provide at least one file.",
                                  code='invalid')
        if bool(cv1):
            if cv1.size > 1024*1024:
                raise forms.ValidationError(
                    'File size must be under %s' %(filesizeformat(1024*1024))
                )
        if bool(cv2):
            if cv2.size > 1024*1024:
                raise forms.ValidationError(
                    'File size must be under %s' % (filesizeformat(1024*1024))
                )
        return cleaned_data


class CompanySignup(forms.ModelForm):

    username = forms.CharField(max_length=50)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password "
                                          "as before, for verification.")

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    layout = Layout(
        Fieldset('Select Username and Password',
                 'username', 'password1', 'password2'),
        Fieldset('Company Details',
                 'company_name', 'description', 'postal_address',
                 'website', 'office_contact_no',
                 Row(Span6('organization_type'), Span6('industry_sector'))),
        Fieldset('First Point of Contact',
                 'head_hr_name', 'head_hr_email', 'head_hr_mobile',
                 'head_hr_designation', 'head_hr_fax'),
        Fieldset('Second Point of Contact',
                 'first_hr_name', 'first_hr_email', 'first_hr_mobile',
                 'first_hr_designation', 'first_hr_fax')
    )

    class Meta:
        model = Company
        fields = ['company_name', 'description', 'postal_address', 'website',
                  'organization_type', 'industry_sector', 'office_contact_no',
                  'head_hr_name', 'head_hr_email', 'head_hr_designation',
                  'head_hr_mobile', 'head_hr_fax', 'first_hr_name',
                  'first_hr_email', 'first_hr_designation', 'first_hr_fax',
                  'first_hr_mobile']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'postal_address': forms.Textarea(attrs={'rows': 4})
        }

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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            UserProfile.objects.get(username=username)
            raise ValidationError("This username already exists. Please "
                                  "select different username.")
        except UserProfile.DoesNotExist:
            pass
        return username


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

    layout = Layout(
            Row('title'),
            Row(Span6('event_type'), Span6('duration')),
            Row('logistics'),
            Row('remark')
    )

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


class AdminEventForm(forms.ModelForm):

    layout = Layout(
        Row('title'),
        Row(Span6('event_type'), Span6('duration')),
        Row('logistics'),
        Row('remark'),
        Row('is_approved', 'final_date')
    )

    class Meta:
        model = Event
        fields = ['title', 'event_type', 'duration', 'logistics', 'remark',
                  'is_approved', 'final_date']
        widgets = {
            'logistics': forms.Textarea(attrs={'rows': 4}),
            'remark': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(AdminEventForm, self).__init__(*args, **kwargs)
        self.fields['title'].disabled = True

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
                      "'Approved Date' or leave both unchanged."
            raise forms.ValidationError(err_msg)


class ProgrammeForm(forms.ModelForm):

    layout = Layout(
        Fieldset(
            "Year, Department and Programme Name",
            'year', 'dept', 'discipline', 'name',
        ),
        Fieldset(
            "Minor status (Check if this programme is a Minor programme)",
            'minor_status'
        ),
        Fieldset(
            "Open for Placement/Internships",
            Row('open_for_placement'),
            Row('open_for_internship')
        )
    )

    class Meta:
        model = Programme
        fields = '__all__'


class StudentProfileUploadForm(forms.Form):

    layout = Layout(
        Fieldset("Content of CSV File",
                 Row('job_candidate'), Row('intern_candidate')),
        Fieldset("Select CSV File", 'csv')
    )

    csv = forms.FileField(required=True, allow_empty_file=True,
                          label='Upload CSV')

    job_candidate = forms.BooleanField(required=True, initial=True,
                                       label='List of Job candidates')
    intern_candidate = forms.BooleanField(required=False, initial=True,
                                          label='List of Intern candidates')

    def clean(self):
        cleaned_data = super(StudentProfileUploadForm, self).clean()
        job_candidate = cleaned_data['job_candidate']
        intern_candidate = cleaned_data['intern_candidate']
        if job_candidate and intern_candidate:
            raise ValidationError("Select only one option: Job or Intern")
        if not bool(job_candidate) and not bool(intern_candidate):
            raise ValidationError("Select one option: Job or Intern")


class StudentFeeCSVForm(forms.Form):

    csv = forms.FileField(required=False, allow_empty_file=True,
                          label='Upload CSV')


class StudentDetailDownloadForm(forms.Form):
    name = forms.BooleanField(initial=True, required=False)
    iitg_webmail = forms.BooleanField(initial=False, required=False,
                                      label='IITG Webmail')
    roll_no = forms.BooleanField(initial=True, required=True, label='Roll No')
    cpi = forms.BooleanField(initial=False, required=False)
    dob = forms.BooleanField(initial=False, required=False, label='DOB')
    sex = forms.BooleanField(initial=False, required=False, label='Gender')
    category = forms.BooleanField(initial=False, required=False)
    nationality = forms.BooleanField(initial=False, required=False)
    minor_year = forms.BooleanField(initial=False, required=False,
                                    label='Minor Year')
    minor_dept = forms.BooleanField(initial=False, required=False,
                                    label='Minor Departent')
    minor_prog = forms.BooleanField(initial=False, required=False,
                                    label='Minor Programme')
    minor_discipline = forms.BooleanField(initial=False, required=False,
                                          label='Minor Discipline')
    year = forms.BooleanField(initial=False, required=False,
                              label='Major Year')
    dept = forms.BooleanField(initial=False, required=False,
                              label='Major Department')
    prog = forms.BooleanField(initial=False, required=False,
                              label='Major Programme')
    discipline = forms.BooleanField(initial=False, required=False,
                                    label='Major Discipline')
    hostel = forms.BooleanField(required=False, initial=False, label='Hostel')
    room_no = forms.BooleanField(required=False, initial=False,
                                 label='Room No')
    alternative_email = forms.BooleanField(required=False, initial=False,
                                           label='Alternative Email')
    mobile_campus = forms.BooleanField(required=False, initial=False,
                                       label='Mobile (Campus)')
    mobile_campus_alternative = forms.BooleanField(
        initial=False, required=False, label='Mobile Alternative (Campus)')
    mobile_home = forms.BooleanField(initial=False, required=False,
                                     label='Mobile Home')
    percentage_x = forms.BooleanField(initial=False, required=False,
                                      label='Percentage X')
    percentage_xii = forms.BooleanField(initial=False, required=False,
                                        label='Percentage XII')
    board_x = forms.BooleanField(initial=False, required=False,
                                 label='X Examination Board')
    board_xii = forms.BooleanField(initial=False, required=False,
                                   label='XII Examination Board')
    medium_x = forms.BooleanField(initial=False, required=False,
                                  label='X Examination Medium')
    medium_xii = forms.BooleanField(initial=False, required=False,
                                    label='XII Examination Medium')
    passing_year_x = forms.BooleanField(initial=False, required=False,
                                        label='X Examination Passing Year')
    passing_year_xii = forms.BooleanField(initial=False, required=False,
                                          label='XII Examination Passing Year')
    gap_in_study = forms.BooleanField(initial=False, required=False,
                                      label='Gap in study')
    jee_air_rank = forms.BooleanField(initial=False, required=False,
                                      label='JEE/GATE/JAM Rank or MA Marks')
    rank_category = forms.BooleanField(initial=False, required=False,
                                       label='Rank Category')
    pd_status = forms.BooleanField(initial=False, required=False,
                                   label='Physical Disability')
    spi_1_sem = forms.BooleanField(initial=False, required=False,
                                   label='SPI 1st Sem')
    spi_2_sem = forms.BooleanField(initial=False, required=False,
                                   label='SPI 2nd Sem')
    spi_3_sem = forms.BooleanField(initial=False, required=False,
                                   label='SPI 3rd Sem')
    spi_4_sem = forms.BooleanField(initial=False, required=False,
                                   label='SPI 4th Sem')
    spi_5_sem = forms.BooleanField(initial=False, required=False,
                                   label='SPI 5th Sem')
    spi_6_sem = forms.BooleanField(initial=False, required=False,
                                   label='SPI 6th Sem')
    fee_transaction_id = forms.BooleanField(initial=False, required=False,
                                            label='Fee Transaction ID')

    layout = Layout(
        Fieldset(
            'Basic Information',
            Row('roll_no'),
            Row('name', 'iitg_webmail'),
            Row('sex'),
            Row('dob'),
            Row('category', 'nationality'),
            Row('pd_status'),
            Row('fee_transaction_id'),
            Row('hostel', 'room_no'),
        ),
        Fieldset(
            'Contact',
            Row('mobile_campus', 'mobile_campus_alternative', 'mobile_home'),
        ),
        Fieldset(
            'Major/Minor Programmes',
            Row('minor_year', 'year'),
            Row('minor_dept', 'dept'),
            Row('minor_prog', 'prog'),
            Row('minor_discipline', 'discipline'),
        ),
        Fieldset(
            'Board Exams',
            Row('percentage_x', 'percentage_xii'),
            Row('board_x', 'board_xii'),
            Row('medium_x', 'medium_xii'),
            Row('passing_year_x', 'passing_year_xii'),
            Row('gap_in_study'),
            Row('jee_air_rank', 'rank_category'),
        ),
        Fieldset(
            'CPI',
            Row('spi_1_sem', 'spi_2_sem'),
            Row('spi_3_sem', 'spi_4_sem'),
            Row('spi_5_sem', 'spi_6_sem'),
        )
    )

    def clean(self):
        cleaned_data = self.cleaned_data

        if not cleaned_data.get('roll_no'):
            raise ValidationError('Roll No cannot be left unselected.')

        all_fields_false = True
        for field_value in cleaned_data.values():
            if bool(field_value):
                all_fields_false = False
                break

        if all_fields_false:
            raise ValidationError('Select at least one field.')
        return self.cleaned_data


class CompanyDetailDownloadForm(forms.Form):
    company_name = forms.BooleanField(initial=True, required=True,
                                      label='Company Name')
    website = forms.BooleanField(initial=False, required=False,
                                 label='website')
    office_contact_no = forms.BooleanField(initial=False, required=False,
                                           label='Office Contact Number')
    organization_type = forms.BooleanField(initial=False, required=False,
                                           label='Organization Type')
    industry_sector = forms.BooleanField(initial=False, required=False,
                                         label='Industry Sector')
    head_hr_name = forms.BooleanField(initial=False, required=False,
                                      label='1st HR Name')
    head_hr_mobile = forms.BooleanField(initial=False, required=False,
                                        label='1st HR Mobile')
    head_hr_designation = forms.BooleanField(initial=False, required=False,
                                             label='1st HR Designation')
    head_hr_email = forms.BooleanField(initial=False, required=False,
                                       label='1st HR Email')
    head_hr_fax = forms.BooleanField(initial=False, required=False,
                                     label='1st HR Fax')
    first_hr_name = forms.BooleanField(initial=False, required=False,
                                       label='2nd HR Name')
    first_hr_mobile = forms.BooleanField(initial=False, required=False,
                                         label='2nd HR Mobile')
    first_hr_designation = forms.BooleanField(initial=False, required=False,
                                              label='2nd HR Designation')
    first_hr_email = forms.BooleanField(initial=False, required=False,
                                        label='2nd HR Email')
    first_hr_fax = forms.BooleanField(initial=False, required=False,
                                      label='2nd HR Fax')

    layout = Layout(
        Fieldset(
            'Company Details',
            Row('company_name', 'website'),
            Row('organization_type', 'industry_sector'),
            Row('office_contact_no'),
        ),
        Fieldset(
            'HR Details',
            Row('head_hr_name', 'first_hr_name'),
            Row('head_hr_mobile', 'first_hr_mobile'),
            Row('head_hr_designation', 'first_hr_designation'),
            Row('head_hr_email', 'first_hr_email'),
            Row('head_hr_fax', 'first_hr_fax'),
        )
    )

    def clean(self):
        cleaned_data = self.cleaned_data

        if not cleaned_data.get('company_name'):
            raise ValidationError('Company Name cannot be left unselected.')

        all_fields_false = True
        for field_value in cleaned_data.values():
            if bool(field_value):
                all_fields_false = False
                break

        if all_fields_false:
            raise ValidationError('Select at least one field.')
        return self.cleaned_data
