import csv
import os
import random
import string
import StringIO
import zipfile

from django.db import IntegrityError

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.encoding import smart_str
from django.views.generic import (View, ListView, DetailView, TemplateView,
                                  UpdateView, FormView)

from .models import (Admin, Student, Company, Job, StudentJobRelation, CV,
                     Avatar, Signature, Programme, ProgrammeJobRelation,
                     UserProfile, Event)
from .forms import (AdminJobEditForm, StudentSearchForm, StudentDebarForm,
                    AdminEventForm, StudentProfileUploadForm,
                    StudentFeeCSVForm, StudentDetailDownloadForm,
                    CompanyDetailDownloadForm, ShortlistCSVForm,
                    CompanyProfileEdit, SelectJobForm, StudentRollNoFormSet)

from .constants import CATEGORY


class HomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    login_url = reverse_lazy('login')
    template_name = 'jobportal/Admin/home.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['admin'] = Admin.objects.get(user=self.request.user)
        return context


class ProgrammeList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = Programme.objects.all()
    template_name = 'jobportal/Admin/programme_list.html'
    context_object_name = 'programme_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class CompanySignupList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = Company.objects.filter(user__is_active=False)
    template_name = 'jobportal/Admin/company_signup_list.html'
    context_object_name = 'company_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class CompanyList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = Company.objects.filter(user__is_active=True)
    template_name = 'jobportal/Admin/company_list.html'
    context_object_name = 'company_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class CompanyDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View class that renders details of Company instance from Admin User's
    account.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    model = Company
    template_name = 'jobportal/Admin/company_detail.html'
    context_object_name = 'company'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_object(self, queryset=None):
        return Company.objects.select_related('user').get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(CompanyDetail, self).get_context_data(**kwargs)
        context['job_list'] = Job.objects.filter(company_owner=self.object)
        return context


class CompanyUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View class that handles updating Company instance from Admin User's
    account.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    form_class = CompanyProfileEdit
    model = Company
    template_name = 'jobportal/Admin/company_update.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_success_url(self):
        return reverse_lazy('admin-company-detail', args=(self.object.id,))


class CompanyApprove(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request, pk):
        company = Company.objects.get(id=pk)
        if company.user is not None and company.user.is_active is False:
            company.user.is_active = True
            company.user.save()
            admin_id = self.request.session['admin_instance_id']
            company.approver = Admin.objects.get(id=admin_id)
            company.approval_date = timezone.now()
            company.save()
        return redirect('admin-company-detail', pk=company.id)


class JobList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View that renders all approved Job instances for Admin Users.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    queryset = Job.objects.select_related('company_owner').filter(approved=True)
    template_name = 'jobportal/Admin/job_list.html'
    context_object_name = 'job_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class JobListCSV(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View class for downloading CSV of all Jobs.
    """
    login_url = reverse_lazy('login')
    raise_exception = False
    template_name = 'jobportal/Admin/job_download.html'

    def test_func(self):
        """
        Check if user is allowed to perform the action.
        :return: True if User is allowed else False.
        """
        # user is company
        is_admin = self.request.user.user_type == 'admin'
        if not is_admin:
            return False
        return True

    def get(self, request, get_page='page'):
        """
        Returns a CSV containing job details.
        :param request: HttpRequest object
        :param get_page: string
        :return: HttpResponse object
        """
        if get_page == 'page':
            return render(request, self.template_name, dictionary=None)
        elif get_page == 'file':
            file_name = 'JobList_{}.csv'.format(smart_str(timezone.now().date()))
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; ' \
                                              'filename=%s' % file_name
            wr = csv.writer(response, quoting=csv.QUOTE_ALL)
            headers = ['Company', 'designation', 'Profile', 'Openings',
                       'CPI Shortlist', 'Minimum CPI', 'Backlog Filter',
                       'Backlogs Allowed', 'Percentage X', 'Percentage XII',
                       'CTC BTECH', 'Gross BTECH', 'CTC MTECH', 'Gross MTECH',
                       'CTC MA', 'Gross MA', 'CTC MSC', 'Gross MSC',
                       'CTC MSR', 'Gross MSR', 'CTC PHD', 'Gross PHD',
                       'Approval Status','Opening DateTime', 'Closing DateTime']
            wr.writerow(headers)
            job_list = Job.objects.all()
            for job in job_list:
                row = [
                    smart_str(job.company_owner.company_name),
                    smart_str(job.designation),
                    smart_str(job.profile_name),
                    smart_str(job.num_openings),
                    smart_str(job.cpi_shortlist),
                    smart_str(job.minimum_cpi),
                    smart_str(job.backlog_filter),
                    smart_str(job.num_backlogs_allowed),
                    smart_str(job.percentage_x),
                    smart_str(job.percentage_xii),
                    smart_str(job.ctc_btech),
                    smart_str(job.gross_btech),
                    smart_str(job.ctc_mtech),
                    smart_str(job.gross_mtech),
                    smart_str(job.ctc_ma),
                    smart_str(job.gross_ma),
                    smart_str(job.ctc_msc),
                    smart_str(job.gross_msc),
                    smart_str(job.ctc_msr),
                    smart_str(job.gross_msr),
                    smart_str(job.ctc_phd),
                    smart_str(job.gross_phd),
                    smart_str(job.approved),
                    smart_str(job.opening_datetime),
                    smart_str(job.application_deadline),
                ]
                wr.writerow(row)
            return response
        else:
            return Http404()


class JobListUnapproved(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View that renders all unapproved Job instances for Admin Users.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    queryset = Job.objects.select_related('company_owner').exclude(
        approved=True)
    template_name = 'jobportal/Admin/job_list_unapproved.html'
    context_object_name = 'job_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class JobDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View that renders details of Job instance for Admin users.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    model = Job
    template_name = 'jobportal/Admin/job_detail.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_context_data(self, **kwargs):
        context = super(JobDetail, self).get_context_data(**kwargs)
        context['rel_list'] = ProgrammeJobRelation.objects.filter(
            job=self.object)
        return context


class JobUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    form_class = AdminJobEditForm
    template_name = 'jobportal/Admin/job_update.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_object(self, queryset=None):
        return Job.objects.select_related('company_owner').get(
            id=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse_lazy('admin-job-detail', args=(self.object.id,))


class JobProgrammeUpdate(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Renders a list of all programmes available for placement and saves the
    selected programmes as programmes which are related with a Job object on
    submission.
    """
    login_url = reverse_lazy('login')
    raise_exception = True
    template_name = 'jobportal/Admin/jobprog_list_update.html'
    job = None

    def test_func(self):
        self.job = get_object_or_404(Job, id=self.kwargs['jobpk'])
        is_admin = self.request.user.user_type == 'admin'
        if not is_admin:
            return False
        return True

    def get(self, request, jobpk):
        # TODO: Integrate saved_jobrels when MDL is completed
        saved_jobrels = [jobrel.prog.id for jobrel in
                         ProgrammeJobRelation.objects.filter(job__id=jobpk)]
        minor_list = Programme.objects.filter(open_for_placement=True,
                                              minor_status=True)
        btech_bdes_list = Programme.objects.filter(
            open_for_placement=True, minor_status=False
        ).filter(
            Q(name='BTECH') | Q(name='BDES')
        )

        mtech_mdes_list = Programme.objects.filter(
            open_for_placement=True,
            minor_status=False
        ).filter(
            Q(name='MTECH') | Q(name='MDES')
        )

        phd_list = Programme.objects.filter(open_for_placement=True,
                                            minor_status=False,
                                            name='PHD')
        ma_list = Programme.objects.filter(open_for_placement=True,
                                           minor_status=False,
                                           name='MA')
        msc_list = Programme.objects.filter(open_for_placement=True,
                                            minor_status=False,
                                            name='MSC')
        msr_list = Programme.objects.filter(open_for_placement=True,
                                            minor_status=False,
                                            name='MSR')
        args = dict(minor_list=minor_list, btech_bdes_list=btech_bdes_list,
                    ma_list=ma_list, mtech_mdes_list=mtech_mdes_list,
                    msc_list=msc_list, phd_list=phd_list, jobpk=jobpk,
                    saved_jobrels=saved_jobrels, msr_list=msr_list)
        return render(request, self.template_name, args)

    def post(self, request, jobpk):

        job = get_object_or_404(Job, id=jobpk)

        minor_list_ids = request.POST.getlist('selected_minor_ids')
        btech_bdes_list = request.POST.getlist('selected_btech_bdes_ids')
        mtech_mdes_list_ids = request.POST.getlist('selected_mtech_mdes_ids')
        phd_list_ids = request.POST.getlist('selected_phd_ids')
        ma_list_ids = request.POST.getlist('selected_ma_ids')
        msc_list_ids = request.POST.getlist('selected_msc_ids')
        msr_list_ids = request.POST.getlist('selected_msr_ids')

        programme_list = Programme.objects.filter(
            Q(id__in=minor_list_ids) |
            Q(id__in=btech_bdes_list) |
            Q(id__in=phd_list_ids) |
            Q(id__in=ma_list_ids) |
            Q(id__in=mtech_mdes_list_ids) |
            Q(id__in=msc_list_ids) |
            Q(id__in=msr_list_ids)
        )

        for programme in programme_list:
            ProgrammeJobRelation.objects.get_or_create(
                job=job,
                prog=programme
            )
        return redirect('admin-job-detail', pk=job.id)


class JobApprove(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request, pk):
        job = get_object_or_404(Job, id=pk)
        if job.approved is not True:
            job.approved = True
            job.approved_on = timezone.now()
            job.save()
        return redirect('admin-job-detail', pk=pk)


class JobRelList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Displays list of candidates for a particular Job object.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    template_name = 'jobportal/Admin/jobrel_list.html'
    context_object_name = 'rel_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_queryset(self):
        return StudentJobRelation.objects.select_related('stud').filter(
            job__id=self.kwargs['pk'], is_debarred=False)

    def get_context_data(self, **kwargs):
        context = super(JobRelList, self).get_context_data(**kwargs)
        context['job'] = Job.objects.select_related('company_owner').get(
            id=self.kwargs['pk']
        )
        return context


class JobRelListCSV(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View class which handles downloading list of candidates for a Job
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False

    def test_func(self):
        """
        Check if user is allowed to perform the action.
        :return: True if User is allowed else False.
        """
        return self.request.user.user_type == 'admin'

    @staticmethod
    def get(request, pk):
        """
        Returns the CSV containing applicant data.
        CSV Fields:
            1. Roll No
            2. Name
            3. Web-mail
            4. Gender
            5. Department
            6. Discipline (Specialization or Branch)
            7. Program
            8. CPI
            9. Percentage X
            10. Percentage XII
            11. Mobile (IITG Campus)
            12. Alternate Email
        :param request: HttpRequest object
        :param pk: id of Job object
        :return: HttpResponse object
        """
        job = get_object_or_404(Job, id=pk)
        company_name = str(job.company_owner.company_name).replace(' ', '_')
        file_name = '{}_{}_list.csv'.format(smart_str(company_name), pk)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; ' \
                                          'filename=%s' % file_name
        wr = csv.writer(response, quoting=csv.QUOTE_ALL)
        headers = ['Roll No', 'Name', 'Web-mail', 'Gender', 'Department',
                   'Branch/Specialization', 'Programme', 'CPI', 'Percentage X',
                   'Percentage XII']
        wr.writerow(headers)
        stud_rel_list = StudentJobRelation.objects.filter(job__id=pk)
        for stud_rel in stud_rel_list:
            row = [
                smart_str(stud_rel.stud.roll_no),
                smart_str(stud_rel.stud.name),
                smart_str(stud_rel.stud.iitg_webmail),
                smart_str(stud_rel.stud.sex),
                smart_str(stud_rel.stud.dept),
                smart_str(stud_rel.stud.discipline),
                smart_str(stud_rel.stud.prog),
                smart_str(stud_rel.stud.cpi),
                smart_str(stud_rel.stud.percentage_x),
                smart_str(stud_rel.stud.percentage_xii),
                smart_str(stud_rel.stud.mobile_campus),
                smart_str(stud_rel.stud.alternative_email),
            ]
            wr.writerow(row)
        return response


class StudentList(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """
    View that renders a form for searching a student and displays all matching
    results on submission for Admin Users.
    """
    login_url = reverse_lazy('login')
    # render login page instead of error 403
    raise_exception = False
    form_class = StudentSearchForm
    template_name = 'jobportal/Admin/student_list.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def form_valid(self, form):
        name = form.cleaned_data.get('name', None)
        username = form.cleaned_data.get('username', None)
        roll_no = form.cleaned_data.get('roll_no', None)
        stud_list = Student.objects.all()
        if name is not None:
            stud_list = stud_list.filter(name__icontains=name)
        if username != '' and username is not None:
            stud_list = stud_list.filter(user__username=username)
        if roll_no is not None:
            stud_list = stud_list.filter(roll_no=roll_no)
        args = dict(form=form, stud_list=stud_list)
        return render(self.request, self.template_name, args)


class StudentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    All details of student.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    model = Student
    template_name = 'jobportal/Admin/student_detail.html'
    context_object_name = 'student'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_object(self, queryset=None):
        return Student.objects.get(id=self.kwargs.get('pk', None))
    
    def get_context_data(self, **kwargs):
        context = super(StudentDetail, self).get_context_data(**kwargs)
        context['job_list'] = StudentJobRelation.objects.filter(stud__id=
                                                                self.object.id)
        # Add cv, avatar, sign, rel_list to context
        try:
            context['cv'] = CV.objects.get(stud__id=self.object.id)
        except CV.DoesNotExist:
            context['cv'] = None
        try:
            context['avatar'] = Avatar.objects.get(stud__id=self.object.id)
        except Avatar.DoesNotExist:
            context['avatar'] = None
        try:
            context['sign'] = Signature.objects.get(stud__id=self.object.id)
        except Signature.DoesNotExist:
            context['sign'] = None
        context['rel_list'] = StudentJobRelation.objects.filter(
            stud__id=self.object.id)
        return context


class JobRelListUnapproved(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Lists all placement requests from Companies.
    """
    login_url = reverse_lazy('login')
    context_object_name = 'rel_list'
    template_name = 'jobportal/Admin/jobrel_list_unapproved.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_queryset(self):
        return StudentJobRelation.objects.filter(
            Q(placed_approved__isnull=True, placed_init=True))


class JobRelListDebarred(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    raise_exception = False
    template_name = 'jobportal/Admin/jobrel_list_debarred.html'
    model = StudentJobRelation

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request):
        form = StudentDebarForm()
        rel_list = StudentJobRelation.objects.filter(is_debarred=True)
        args = dict(rel_list=rel_list, form=form)
        return render(request, self.template_name, args)

    def post(self, request):
        form = StudentDebarForm(request.POST)
        if form.is_valid():
            roll_no = form.cleaned_data.get('roll_no', None)
            stud = Student.objects.get(roll_no=roll_no)
            job = form.cleaned_data.get('job', None)
            studjobrel, created = StudentJobRelation.objects.get_or_create(
                stud=stud, job=job)
            if not studjobrel.is_debarred:
                studjobrel.is_debarred = True
                studjobrel.save()
            return redirect('admin-jobrel-list-debarred')
        else:
            rel_list = StudentJobRelation.objects.filter(is_debarred=True)
            args = dict(rel_list=rel_list, form=form)
            return render(request, self.template_name, args)


class StudJobRelPlaceApprove(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Once a company sends a placment request for a candidate, Administrator can
    approve/reject that request.
    """

    login_url = reverse_lazy('login')
    raise_exception = True

    def test_func(self):
        is_admin = self.request.user.user_type == 'admin'
        if not is_admin:
            return True
        job = get_object_or_404(Job, id=self.kwargs['jobpk'])
        deadline_ok = job.application_deadline < timezone.now()
        if not deadline_ok:
            return False
        return True

    def get(self, request, jobpk, jobrelpk):
        jobrel = get_object_or_404(StudentJobRelation, id=jobrelpk)
        if jobrel.stud.placed:
            msg = 'Candidate is already placed.'
            level = messages.ERROR
        elif jobrel.placed_init and jobrel.placed_approved is not None:
            msg = 'Candidate placement request is already approved/rejected.'
            level = messages.ERROR
        elif jobrel.placed_init and jobrel.placed_approved is None:
            jobrel.placed_approved = True
            jobrel.placed_approved_datetime = timezone.now()
            jobrel.save()

            stud = get_object_or_404(Student, id=jobrel.stud.id)
            stud.placed = True
            stud.save()

            msg = 'Candidate placment request approved.'
            level = messages.SUCCESS
        else:
            msg = 'Something crazy happened. Report bug'
            level = messages.ERROR
        messages.add_message(request=request, level=level, message=msg,
                             fail_silently=True)
        return redirect('admin-jobrel-list-unapproved')


class EventList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View class that renders all Events for Admin Users.
    """
    login_url = reverse_lazy('login')
    model = Event
    template_name = 'jobportal/Admin/event_list.html'
    context_object_name = 'event_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_queryset(self):
        return Event.objects.all().order_by('-creation_datetime')


class EventDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View class that renders details of an Event instance for Admin Users.
    """
    login_url = reverse_lazy('login')
    model = Event
    template_name = 'jobportal/Admin/event_detail.html'
    context_object_name = 'event'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_object(self, queryset=None):
        return get_object_or_404(Event, id=self.kwargs['pk'])


class EventUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Renders pre-filled for an already existing event object and saves the
    updates on submission.
    """
    login_url = reverse_lazy('login')
    form_class = AdminEventForm
    template_name = 'jobportal/Admin/event_update.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_object(self, queryset=None):
        return get_object_or_404(Event, id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('admin-event-detail', args=(self.object.id,))
        # return reverse_lazy('admin-event-list')

    def form_valid(self, form):
        form.save()
        return super(EventUpdate, self).form_valid(form)


class UploadStudentData(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Administrator can add students to portal by uploading a CSV (format
    described below). Students will not be able to login just after this step.
    Administrator needs to upload a CSV containing (roll_no, transaction_id)
    pairs to enable logging of Students.
    """
    login_url = reverse_lazy('login')
    template_name = 'jobportal/Admin/student_create.html'
    col_count = 15
    password_len = 8
    # form_class = StudentUploadForm

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def _validate_csv_row(self, row):
        # CSV format
        # Col0: Webmail: no checking
        # Col1: Roll No: Must be number
        # Col2: Name: no checking
        # Col3: Year: Must be in Db
        # Col4: Dept: Must be in Db
        # Col5: Prog: Must be in Db
        # Col6: Discipline: Must be in Db
        # Col7: Minor Year: Must be in Db
        # Col8: Minor Dept: Must be in Db
        # Col9: Minor Prog: Must be in Db
        # Col10: Minor Discipline: Must be in Database
        # Col11: Category: Must be in constants.CATEGORY
        # Col12: CPI: Must be Float
        # Col13: Nationality: NO checking
        # Col14: Gender: Must be in [M, F]
        num_cols = len(row)
        # Check number of columns
        if self.col_count != num_cols:
            return False, 'Total number of columns is not ' + str(
                self.col_count)
        # Check roll no
        try:
            roll_no = int(str(row[1]).strip())
        except ValueError:
            return False, 'Roll number is not a valid number'
        # check year
        if '' in [str(row[3]), str(row[4]), str(row[5]), str(row[6])]:
            return False, 'No programme related fields should be empty.'
        else:
            try:
                year = int(str(row[3]).strip())
            except ValueError:
                return False, 'Year is not a valid number.'
            # get programme
            try:
                dept = str(row[4]).strip()
                prog = str(row[5]).strip().upper()
                Programme.objects.get(year=year, dept=dept,
                                      name=prog, minor_status=False,
                                      discipline__iexact=str(row[6]).strip())
            except Programme.DoesNotExist:
                return False, 'Major Programme %s does not exist in DB' \
                       % str(row[5]).upper()
        # check minor_year
        if '' not in [str(row[7]), str(row[8]), str(row[9]), str(row[10])]:
            try:
                minor_year = int(str(row[7]).strip())
            except ValueError:
                return False, 'Year is not a valid number.'
            try:
                minor_dept = str(row[8])
                minor_prog = str(row[9]).upper()
                Programme.objects.get(year=minor_year, dept=minor_dept,
                                      name=minor_prog, minor_status=True,
                                      discipline__iexact=str(row[10]).strip())
            except Programme.DoesNotExist:
                return False, 'Minor Programme %s does not exist in DB' \
                       % prog
        # check category
        category = str(row[11]).strip()
        if category not in [cat[0] for cat in CATEGORY]:
            return False, 'Invalid Category'
        # check cpi
        try:
            cpi = float(str(row[12]).strip())
        except ValueError:
            return False, 'CPI not a valid number.'
        # check sex/gender
        if str(row[14]).strip() not in ['M', 'F']:
            return False, 'Gender must be M or F only.'

        return True, None

    def get(self, request):
        form = StudentProfileUploadForm()
        return render(request, self.template_name, dict(form=form))

    # TODO: Add Transaction
    def post(self, request):
        form = StudentProfileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            job_candidate = form.cleaned_data.get('job_candidate', None)
            intern_candidate = form.cleaned_data.get('intern_candidate', None)
            csvfile = form.cleaned_data.get('csv', None)
            reader = csv.reader(csvfile, delimiter=',')
            error_rows = error_msg = []
            rowcount = 0
            for row in reader:
                rowcount += 1
                row_ok, error = self._validate_csv_row(row)
                if not row_ok:
                    error_rows.append(rowcount)
                    error_msg.append(error)
                    continue
                username = str(row[0]).strip()
                # dummy password
                password = ''.join(
                    random.SystemRandom().choice(
                        string.ascii_uppercase + string.digits)
                    for _ in range(self.password_len))
                try:
                    userprofile = UserProfile.objects.get(
                        username=username, user_type='student'
                    )
                    error_rows.append(rowcount)
                    error = 'username %s already exists' % username
                    error_msg.append(error)
                except UserProfile.DoesNotExist:
                    userprofile = UserProfile.objects.create(
                        username=username,
                        password=make_password(password=username),
                        is_active=False,
                        user_type='student'
                    )
                    try:
                        year = prog = dept = discipline = None
                        if '' not in [row[3], row[4], row[5], row[6]]:
                            year = int(row[3])
                            dept = str(row[4]).strip()
                            name = str(row[5]).strip()
                            discipline = str(row[6]).strip()
                            prog = Programme.objects.get(
                                year=year, dept=dept, name=name,
                                minor_status=False,
                                discipline__iexact=discipline)

                        minor_year = minor_dept = minor_prog = None
                        minor_discipline = None
                        if '' not in [row[7], row[8], row[9], row[10]]:
                            minor_year = int(row[7])
                            minor_dept = str(row[8]).strip()
                            name = str(row[9]).strip()
                            minor_discipline = str(row[10]).strip()
                            minor_prog = Programme.objects.get(
                                year=minor_year, dept=minor_dept,
                                name=name, minor_status=True,
                                discipline__iexact=str(row[10]).strip())

                        stud = Student.objects.create(
                            user=userprofile,
                            iitg_webmail=str(username) + '@iitg.ac.in',
                            roll_no=int(str(row[1]).strip()),
                            name=str(row[2]).strip(),
                            year=year,
                            dept=dept,
                            prog=prog.name,
                            discipline=discipline,
                            category=str(row[11]).upper(),
                            cpi=float(row[12]),
                            nationality=str(row[13]).strip(),
                            sex=str(row[14]).upper().strip(),
                            job_candidate=job_candidate,
                            intern_candidate=intern_candidate
                        )
                        if minor_year and minor_dept and minor_year:
                            stud.minor_year = minor_year
                            stud.minor_dept = minor_dept
                            stud.minor_prog = minor_prog.name
                            stud.minor_discipline = minor_discipline
                            stud.save()
                    except IntegrityError:
                        userprofile.delete()
                        error = 'Student creation failed. IntegrityError'
                        error_rows.append(rowcount)
                        error_msg.append(error)
                    except ValueError:
                        userprofile.delete()
                        error = 'Student creation failed. ValueError'
                        error_rows.append(rowcount)
                        error_msg.append(error)
                    except TypeError:
                        userprofile.delete()
                        error = 'Student creation failed. TypeError'
                        error_rows.append(rowcount)
                        error_msg.append(error)

            zipped_data = zip(error_rows, error_msg)
            args = dict(zipped_data=zipped_data, form=form)
            return render(request, self.template_name, args)
        else:
            return render(request, self.template_name, dict(form=form))


class StudentFeeStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Admininstrator can activate login permission for students by uploading a
    CSV containing (roll_no, transaction_id) pairs.
    """

    login_url = reverse_lazy('login')
    raise_exception = True
    template_name = 'jobportal/Admin/student_fee_update.html'
    col_count = 2

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request):
        form = StudentFeeCSVForm(None)
        return render(request, self.template_name, dict(form=form))

    def _validate_csv_row(self, row):
        if len(row) != self.col_count:
            return False, "Row does not have two rows"
        try:
            roll_no = int(row[0])
        except ValueError:
            return False, "Roll Number is not a valid number."
        return True, None

    def post(self, request):
        form = StudentFeeCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csvfile = form.cleaned_data['csv']
            reader = csv.reader(csvfile, delimiter=',')
            error_rows = []
            error_msg = []
            rowcount = 0
            for row in reader:
                rowcount += 1
                row_ok, error = self._validate_csv_row(row)
                if not row_ok:
                    error_rows.append(rowcount)
                    error_msg.append(error)
                    continue
                try:
                    stud = Student.objects.get(roll_no=int(row[0]))
                except Student.DoesNotExist:
                    error_rows.append(rowcount)
                    error = 'No student with this roll number found in DB'
                    error_msg.append(error)
                    continue
                userprofile = stud.user
                userprofile.is_active = True
                userprofile.save()
                stud.fee_transaction_id = str(row[1])
                stud.save()
            zipped_data = zip(error_rows, error_msg)
            return render(request, self.template_name,
                          dict(form=form, zipped_data=zipped_data))
        else:
            return render(request, self.template_name, dict(form=form))


class DownloadBondDocument(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.user_type == 'admin'

    @staticmethod
    def get(request, pk):
        job = get_object_or_404(Job, id=pk)
        response = HttpResponse(job.bond_link, content_type='application/pdf')
        download_name = job.company_owner.user.username + '_' + job.designation
        response['Content-Disposition'] = 'attachment; filename=%s' % \
                                          smart_str(download_name)
        return response


class DownloadStudCV(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.user_type == 'admin'

    @staticmethod
    def get(request, pk, cvno):
        cv = get_object_or_404(CV, stud__id=pk)
        if cvno == '1' and bool(cv.cv1.name):
            response = HttpResponse(cv.cv1,
                                    content_type='application/pdf')
            download_name = 'CV1_' + str(cv.stud.roll_no) + '_IITG.pdf'
            response['Content-Disposition'] = 'attachment; filename=%s' % \
                                              smart_str(download_name)
            return response
        elif cvno == '2' and bool(cv.cv2.name):
            response = HttpResponse(cv.cv2,
                                    content_type='application/pdf')
            download_name = 'CV2_' + str(cv.stud.roll_no) + '_IITG.pdf'
            response['Content-Disposition'] = 'attachment; filename=%s' % \
                                              smart_str(download_name)
            return response
        else:
            raise Http404()


class DownloadStudList(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'jobportal/Admin/student_download.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request):
        form = StudentDetailDownloadForm(None)
        return render(request, self.template_name, dict(form=form))

    def post(self, request):
        form = StudentDetailDownloadForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; ' \
                                              'filename="studdetails.csv"'
            wr = csv.writer(response, quoting=csv.QUOTE_NONE)

            # write header row
            headers = []
            for k, v in cleaned_data.iteritems():
                if v:
                    headers.append(k)
            wr.writerow(headers)

            # queyset for all students
            all_studs = Student.objects.all()
            # iterate over queryset
            for stud in all_studs:
                row = []
                # only add fields asked in form
                for k, v in cleaned_data.iteritems():
                    if v:
                        row.append(smart_str(getattr(stud, k)))
                # write student details to as row to csv
                wr.writerow(row)
            return response
        else:
            return render(request, self.template_name, dict(form=form))


class DownloadCompanyList(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'jobportal/Admin/company_download.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request):
        form = CompanyDetailDownloadForm(None)
        return render(request, self.template_name, dict(form=form))

    def post(self, request):
        form = CompanyDetailDownloadForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; ' \
                                              'filename="companydetails.csv"'
            wr = csv.writer(response, quoting=csv.QUOTE_ALL)
            # write header row
            headers = []
            for k, v in cleaned_data.iteritems():
                if v:
                    headers.append(k)
            wr.writerow(headers)

            # queryset for all companies
            all_companies = Company.objects.all()
            # iterate over queryset
            for company in all_companies:
                row = []
                # only add fields asked in form
                for k, v in cleaned_data.iteritems():
                    if v:
                        row.append(smart_str(getattr(company, k)))
                # write company details to as row to csv
                wr.writerow(row)
            return response
        else:
            return render(request, self.template_name, dict(form=form))


class DownloadCVZip(UserPassesTestMixin, LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.user_type == 'admin'

    @staticmethod
    def get(request, pk):
        job = Job.objects.get(id=pk)
        stud_rel_list = StudentJobRelation.objects.filter(job__id=pk)
        cv_list = []
        for stud_rel in stud_rel_list:
            try:
                cv = CV.objects.get(stud=stud_rel.stud)
                cv_path = None
                if bool(stud_rel.cv1):
                    cv_path = cv.cv1.path
                if bool(stud_rel.cv2):
                    cv_path = cv.cv2.path
                if cv_path is not None:
                    cv_list.append(cv_path)
            except CV.DoesNotExist:
                pass

        zip_filename = "IITG_%s_CV.zip" % smart_str(job.id)

        s = StringIO.StringIO()

        zf = zipfile.ZipFile(s, mode="w")
        for cv_path in cv_list:
            cv_dir, cv_name = os.path.split(cv_path)
            # rename filename in archive
            cv_name = 'IITG_' + cv_name[:9] + '.pdf'
            zf.write(cv_path, cv_name)
        zf.close()

        resp = HttpResponse(s.getvalue(),
                            content_type="application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        return resp


class ShortlistCSV(LoginRequiredMixin, UserPassesTestMixin, FormView):

    login_url = reverse_lazy('login')
    template_name = 'jobportal/Admin/jobrel_shortlist_csv.html'
    form_class = ShortlistCSVForm

    def test_func(self):
        return self.request.user.user_type == 'admin'

    @staticmethod
    def _validate_row(row):
        if len(row) != 1:
            return False, 'More than one columns'
        try:
            int(row[0])
        except TypeError:
            return False, 'Failed to convert roll number to integer'
        return True, ''

    def form_valid(self, form):
        csv_file = form.cleaned_data['csv']
        job = form.cleaned_data['job']
        reader = csv.reader(csv_file, delimiter=',')
        error_rows = error_msgs = []
        row_count = 0
        for row in reader:
            row_count += 1
            status, msg = ShortlistCSV._validate_row(row)
            if not status:
                error_rows.append(row_count)
                error_msgs.append(msg)
                continue
            try:
                stud = Student.objects.get(roll_no=row[0])
            except Student.DoesNotExist:
                error_rows.append(row_count)
                msg = 'No student matching roll no {}'.format(row[0])
                error_msgs.append(msg)
                continue
            try:
                stud_job = StudentJobRelation.objects.get(stud=stud, job=job)
                if not stud_job.shortlist_init:
                    stud_job.shortlist_init = True
                    stud_job.shortlist_init_datetime = timezone.now()
                    stud_job.save()
            except StudentJobRelation.DoesNotExist:
                error_rows.append(row_count)
                msg = '{} has not applied for this Job'.format(row[0])
                error_msgs.append(msg)
        errors = zip(error_rows, error_msgs)
        context = dict(form=form, errors=errors)
        return render(self.request, self.template_name, context)


class PlaceStudentView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    raise_exception = False
    template_name = 'jobportal/Admin/place_students.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request):
        job_form = SelectJobForm()
        roll_no_formset = StudentRollNoFormSet()
        context = dict(job_form=job_form, roll_no_formset=roll_no_formset)
        return render(request, self.template_name, context)

    def post(self, request):
        job_form = SelectJobForm(request.POST)
        roll_no_formset = StudentRollNoFormSet(request.POST)
        status_list = []
        if job_form.is_valid() and roll_no_formset.is_valid():
            job = job_form.cleaned_data.get('job', None)
            shortlist_action = job_form.cleaned_data.get('shortlist_action', False)
            apply_action = job_form.cleaned_data.get('apply_action', False)
            formset_data = roll_no_formset.cleaned_data
            for form_data in formset_data:
                roll_no = form_data.get('roll_no', None)
                if roll_no is None:
                    continue
                try:
                    stud = Student.objects.get(roll_no=roll_no)
                except Student.DoesNotExist:
                    status_message = 'Student not found.'
                    status_list.append((roll_no, None, status_message, 'error'))
                    continue
                try:
                    stud_rel = StudentJobRelation.objects.select_related(
                        'stud').get(stud=stud, job=job)
                    if not stud_rel.shortlist_init:
                        if shortlist_action:
                            stud_rel.shortlist_init = True
                            stud_rel.shortlist_init_datetime = timezone.now()
                            stud_rel.placed_init = True
                            stud_rel.placed_init_datetime = timezone.now()
                            stud_rel.placed_approved = True
                            stud_rel.placed_approved_datetime = timezone.now()
                            stud_rel.save()
                            stud.placed = True
                            stud.save()
                            status_message = 'Student has been force shortlisted and placed.'
                            status_list.append((roll_no, stud, status_message, 'success'))
                        else:
                            status_message = 'Student has not been shortlisted.'
                            status_list.append((roll_no, stud, status_message, 'error'))
                    elif not stud.placed:
                        stud_rel.placed_init = True
                        stud_rel.placed_init_datetime = timezone.now()
                        stud_rel.placed_approved = True
                        stud_rel.placed_approved_datetime = timezone.now()
                        stud_rel.save()
                        stud.placed = True
                        stud.save()
                        status_message = 'Student has been successfully placed.'
                        status_list.append((roll_no, stud, status_message, 'success'))
                    else:
                        status_message = 'Student has been already placed.'
                        status_list.append((roll_no, stud, status_message, 'error'))
                except StudentJobRelation.DoesNotExist:
                    if apply_action:
                        stud_rel = StudentJobRelation.objects.create(
                            stud=stud, job=job
                        )
                        status_message = 'Student has been added to candidate list.'
                        status_list.append((roll_no, stud, status_message, 'success'))
                    else:
                        status_message = 'Student has not applied for this Job'
                        status_list.append((roll_no, stud, status_message, 'error'))
            context = dict(job_form=job_form, roll_no_formset=roll_no_formset,
                           status_list=status_list)
            return render(request, self.template_name, context)
        else:
            context = dict(job_form=job_form, roll_no_formset=roll_no_formset)
            return render(request, self.template_name, context)
