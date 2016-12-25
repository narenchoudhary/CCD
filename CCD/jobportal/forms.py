from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from material import *

from models import *


class LoginForm(forms.Form):
    """
    Common Login Form for all Users.
    """
    username = forms.CharField(required=True, label='Username', max_length=50)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(
        required=False, initial=False, label='Remember Me',
        widget=forms.CheckboxInput(attrs={'class': 'filled-in'})
    )


class EditStudProfileForm(forms.ModelForm):
    """
    Modelform that handles profile update for Students.

    Some classes are added to field widgets for materialize.css compatibility.
    """
    class Meta:
        model = Student
        fields = ('dob', 'hostel', 'room_no', 'alternative_email',
                  'mobile_campus', 'mobile_campus_alternative',
                  'mobile_home', 'address_line1', 'address_line2',
                  'address_line3', 'pin_code', 'percentage_x',
                  'percentage_xii', 'board_x', 'board_xii', 'medium_x',
                  'medium_xii', 'passing_year_x', 'passing_year_xii',
                  'gap_in_study', 'gap_reason', 'jee_air_rank',
                  'linkedin_link', 'spi_1_sem', 'spi_2_sem',
                  'spi_3_sem', 'spi_4_sem', 'spi_5_sem', 'spi_6_sem',
                  'active_backlogs', 'rank_category', 'pd_status')

        widgets = {
            # add 'materialize-textarea' for materialize.css
            'gap_reason': forms.Textarea(attrs={
                'class': 'materialize-textarea'
            }),
            # add 'datepicker' for materialize.css
            'dob': forms.DateInput(attrs={
                'class': 'datepicker'
            }),
            # add 'filled-in' for materialize.css
            'gap_in_study': forms.CheckboxInput(attrs={'class': 'filled-in'})
        }


class CompanyJobForm(forms.ModelForm):
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
                  'bond_link', 'additional_info', 'ctc_msr', 'gross_msr']

        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'materialize-textarea'
            }),
            'additional_info': forms.Textarea(attrs={
                'class': 'materialize-textarea'
            }),
            'cpi_shortlist': forms.CheckboxInput(attrs={'class': 'filled-in'}),
            'designation': forms.TextInput(attrs={
                'placeholder': 'Junior Developer'
            }),
            'profile_name': forms.TextInput(attrs={'placeholder': 'SDE'}),
            'num_openings': forms.NumberInput(attrs={'placeholder': '15'})
        }

    def clean_minimum_cpi(self):
        minimum_cpi = self.cleaned_data.get('minimum_cpi', None)
        if minimum_cpi is None or minimum_cpi < 5.00:
            minimum_cpi = 5.00
        return minimum_cpi


class AdminJobEditForm(forms.ModelForm):
    """
    Job ModelForm for Admin Users to create Job instances.
    """

    def __init__(self, *args, **kwargs):
        super(AdminJobEditForm, self).__init__(*args, **kwargs)
        self.fields['designation'].widget.attrs['readonly'] = True
        self.fields['profile_name'].widget.attrs['readonly'] = True

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

        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'materialize-textarea'
            }),
            'additional_info': forms.Textarea(attrs={
                'class': 'materialize-textarea'
            }),
            'cpi_shortlist': forms.CheckboxInput(attrs={'class': 'filled-in'}),
            'backlog_filter': forms.CheckboxInput(attrs={'class': 'filled-in'}),
            'designation': forms.TextInput(attrs={
                'placeholder': 'Junior Developer'
            }),
            'profile_name': forms.TextInput(attrs={'placeholder': 'SDE'}),
            'num_openings': forms.NumberInput(attrs={'placeholder': '15'})
        }

    def clean_minimum_cpi(self):
        minimum_cpi = self.cleaned_data.get('minimum_cpi', None)
        if minimum_cpi is None or minimum_cpi < 5.00:
            minimum_cpi = 5.00
        return minimum_cpi


class CompanyEventForm(forms.Form):

    class Meta:
        model = Event
        fields = ['title', 'event_type', 'event_date1', 'event_date2']


class CompanyProfileEdit(forms.ModelForm):
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
            'description': forms.Textarea(attrs={
                'class': 'materialize-textarea'
            }),
            'postal_address': forms.Textarea(attrs={
                'class': 'materialize-textarea'
            })
        }


class StudentSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100, required=False, label=_('Name (or part of name)'))
    username = forms.CharField(
        max_length=50, label=_('Username'), required=False)
    roll_no = forms.IntegerField(label=_('Roll Number'), required=False)

    def clean(self):
        cleaned_data = super(StudentSearchForm, self).clean()
        name = cleaned_data.get('name', None)
        username = cleaned_data.get('username', None)
        roll_no = cleaned_data.get('roll_no', None)

        if username is None and roll_no is None and name is None:
            raise ValidationError("All fields cannot be empty")
        return cleaned_data


class SelectCVForm(forms.Form):
    """
    CV ModelForm for Student Users to create and update CVs.
    """
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop("extra")
        super(SelectCVForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(extra):
            self.fields['custom_%s' % i] = forms.BooleanField(
                label=str(question).upper(), initial=False, required=False,
                widget=forms.CheckboxInput(attrs={'class': 'filled-in'})
            )

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
        print(true_count)
        print(false_count)
        if true_count is 0 and false_count is not 0:
            raise ValidationError("Select one CV.", code='invalid')
        if true_count is 2 and false_count is 0:
            raise ValidationError("Select only one CV.", code='invalid')
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

    def clean_cv1(self):
        cv1 = self.cleaned_data.get('cv1', None)
        if cv1 is not None:
            if cv1.size > 1024*1024:
                raise forms.ValidationError(
                    'File size must be under %s' %(filesizeformat(1024*1024))
                )
        return cv1

    def clean_cv2(self):
        cv2 = self.cleaned_data.get('cv2', None)
        if cv2 is not None:
            if cv2.size > 1024*1024:
                raise forms.ValidationError(
                    'File size must be under %s' %(filesizeformat(1024*1024))
                )
        return cv2

    def clean(self):
        cleaned_data = super(CVForm, self).clean()
        cv1 = self.cleaned_data.get('cv1', None)
        cv2 = self.cleaned_data.get('cv2', None)
        if cv1 is None and cv2 is None:
            raise ValidationError("Provide at least one file.", code='invalid')
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

    class Meta:
        model = Company
        fields = ['company_name', 'description', 'postal_address', 'website',
                  'organization_type', 'industry_sector', 'office_contact_no',
                  'head_hr_name', 'head_hr_email', 'head_hr_designation',
                  'head_hr_mobile', 'head_hr_fax', 'first_hr_name',
                  'first_hr_email', 'first_hr_designation', 'first_hr_fax',
                  'first_hr_mobile']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'materialize-textarea'
            }),
            'postal_address': forms.Textarea(attrs={
                'class': 'materialize-textarea'
            })
        }
        help_texts = {
            'company_name': 'Full name of the company/firm',
            'description': 'A short description of the company',
            'head_hr_email': 'Registration confirmation will be sent to this '
                             'email address.'
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


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'event_type', 'duration', 'logistics', 'remark']

        widgets = {
                    'logistics': forms.Textarea(attrs={
                        'class': 'materialize-textarea'
                    }),
                    'remark': forms.Textarea(attrs={
                        'class': 'materialize-textarea'
                    })
                }
        help_texts = {
            'logistics': 'Please note that all requested logistics might '
                         'not be available.'
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)


class AdminEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'duration', 'logistics', 'remark',
                  'is_approved', 'final_date']
        widgets = {
            'logistics': forms.Textarea(attrs={
                'class': 'materialize-textarea'
            }),
            'remark': forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'final_date': forms.DateInput(attrs={'class': 'datepicker'}),
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
            raise forms.ValidationError(err_msg, code='invalid')


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
    """
    Form for uploading Student data.
    """
    csv = forms.FileField(
        required=True, allow_empty_file=True, label=_('Upload CSV'))

    job_candidate = forms.BooleanField(
        required=True, initial=True, label=_('Job candidates'),
        widget=forms.CheckboxInput(attrs={'class': 'filled-in'})
    )
    intern_candidate = forms.BooleanField(
        required=False, initial=True, label=_('Intern candidates'),
        widget=forms.CheckboxInput(attrs={'class': 'filled-in'})
    )

    def clean(self):
        cleaned_data = super(StudentProfileUploadForm, self).clean()
        job_candidate = cleaned_data['job_candidate']
        intern_candidate = cleaned_data['intern_candidate']
        if job_candidate and intern_candidate:
            error = "Select only one option: Job Candidate or Intern Candidate"
            raise ValidationError(_(error))
        if not bool(job_candidate) and not bool(intern_candidate):
            error = "Select one option: Job Candidate or Intern Candidate"
            raise ValidationError(_(error))


class StudentFeeCSVForm(forms.Form):
    """
    Form for uploading Student Fee data.
    """
    csv = forms.FileField(required=False, allow_empty_file=True,
                          label='Upload CSV')


class StudentDetailDownloadForm(forms.Form):

    model_fields = ['name', 'roll_no', 'iitg_webmail', 'sex', 'dob', 'category', 'nationality',
                    'hostel', 'room_no', 'pd_status',

                    'minor_year', 'minor_dept', 'minor_prog',
                    'minor_discipline', 'year', 'dept', 'prog', 'discipline',

                    'alternative_email', 'mobile_campus',
                    'mobile_campus_alternative', 'mobile_home',
                    'percentage_x', 'percentage_xii', 'board_x', 'board_xii',

                    'medium_x', 'medium_xii', 'passing_year_x', 'passing_year_xii',
                    'gap_in_study', 'jee_air_rank', 'rank_category',

                    'cpi', 'spi_1_sem', 'spi_2_sem',
                    'spi_3_sem', 'spi_4_sem', 'spi_5_sem', 'spi_6_sem',
                    'active_backlogs']

    def __init__(self, *args, **kwargs):
        super(StudentDetailDownloadForm, self).__init__(*args, **kwargs)
        for field in self.model_fields:
            student_field = Student._meta.get_field(field)
            self.fields[field] = forms.BooleanField(
                initial=False, required=False,
                label=student_field.verbose_name,
                widget=forms.CheckboxInput(attrs={'class': 'filled-in'})
            )
        self.fields['roll_no'].required = True
        self.fields['roll_no'].initial = True


class CompanyDetailDownloadForm(forms.Form):
    """
    Form for Admin Users to download Company details.
    """
    model_fields = ['company_name', 'postal_address', 'website',
                    'organization_type', 'industry_sector',
                    'office_contact_no',
                    'head_hr_name', 'head_hr_email', 'head_hr_designation',
                    'head_hr_mobile', 'head_hr_fax', 'first_hr_name',
                    'first_hr_email', 'first_hr_designation', 'first_hr_fax',
                    'first_hr_mobile']

    def __init__(self, *args, **kwargs):
        super(CompanyDetailDownloadForm, self).__init__(*args, **kwargs)
        for field in self.model_fields:
            company_field = Company._meta.get_field(field)
            self.fields[field] = forms.BooleanField(
                initial=False, required=False,
                label=company_field.verbose_name,
                widget=forms.CheckboxInput(attrs={'class': 'filled-in'})
            )
        self.fields['company_name'].required = True
        self.fields['company_name'].initial = True


class StudentDebarForm(forms.Form):
    job = forms.ModelChoiceField(
        queryset=Job.objects.all().order_by('designation'), label='Job')
    roll_no = forms.DecimalField(
        max_digits=15, decimal_places=0, label='Roll No')

    def clean_roll_no(self):
        roll_no = self.cleaned_data.get('roll_no', None)
        if not Student.objects.filter(roll_no=roll_no).exists():
            raise ValidationError('No student with this roll number exists.')
        return roll_no


class ShortlistCSVForm(forms.Form):
    """
    Form for updating shortlisted Students for a Job through a CSV file.
    """
    job = forms.ModelChoiceField(
        queryset=Job.objects.filter(approved=True).order_by('designation')
    )
    csv = forms.FileField(required=True, allow_empty_file=False,
                          label='Upload CSV')
