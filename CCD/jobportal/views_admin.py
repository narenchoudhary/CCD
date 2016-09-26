import csv
import string
import random

from sqlite3.dbapi2 import IntegrityError

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.encoding import smart_str
from django.views.generic import (View, ListView, CreateView, DetailView,
                                  TemplateView, UpdateView)

from .models import (Admin, Student, Company, Job, StudentJobRelation, CV,
                     Avatar, Signature, Programme, ProgrammeJobRelation,
                     UserProfile, Event)
from .forms import (AdminJobEditForm, StudentSearchForm,
                    EditCompany, ProgrammeForm, AdminEventForm,
                    StudentProfileUploadForm, StudentFeeCSVForm)
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


class ProgrammeCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = ProgrammeForm
    template_name = 'jobportal/Admin/programme_create.html'
    success_url = reverse_lazy('programme-list')

    def test_func(self):
        return self.request.user.user_type == 'admin'


class ProgrammeUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Programme
    fields = '__all__'
    template_name = 'jobportal/Admin/programme_update.html'
    success_url = reverse_lazy('programme-list')

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_object(self, queryset=None):
        return Programme.objects.get(id=self.kwargs['pk'])


class ProgrammePlacementList(LoginRequiredMixin, UserPassesTestMixin,
                             ListView):
    login_url = reverse_lazy('login')
    template_name = 'jobportal/Admin/programme_placement_list.html'
    context_object_name = 'programme_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_queryset(self):
        return Programme.objects.filter(open_for_placement=True)


class ProgrammeInternshipList(LoginRequiredMixin, UserPassesTestMixin,
                              ListView):
    login_url = reverse_lazy('login')
    template_name = 'jobportal/Admin/programme_internship_list.html'
    context_object_name = 'programme_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_queryset(self):
        return Programme.objects.filter(open_for_internship=True)


class CompanySignupList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = Company.objects.filter(approved=None)
    template_name = 'jobportal/Admin/company_signup_list.html'
    context_object_name = 'company_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class CompanyList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = Company.objects.filter(approved=True)
    template_name = 'jobportal/Admin/company_list.html'
    context_object_name = 'company_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class CompanyDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Company
    template_name = 'jobportal/Admin/company_detail.html'
    context_object_name = 'company'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetail, self).get_context_data(**kwargs)
        company_instance = Company.objects.get(id=self.kwargs['pk'])
        context['company'] = company_instance
        context['job_list'] = Job.objects.filter(company_owner=
                                                 company_instance)
        return context


class CompanyUpdate(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    form_class = EditCompany
    model = Company
    template_name = 'jobportal/Admin/company_update.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request, pk):
        company = Company.objects.get(id=pk)
        form = EditCompany(instance=company)
        return render(request, self.template_name,
                      dict(form=form, company=company))

    def post(self, request, pk):
        company = Company.objects.get(id=pk)
        form = EditCompany(request.POST, instance=company)
        approved = company.approved
        if form.is_valid():
            form.save()
            return redirect('admin-company-detail', pk=company.id)
        else:
            return render(request, self.template_name, dict(form=form))


class CompanyApprove(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request, pk):
        company = Company.objects.get(id=pk)
        user = company.user
        if user is not None and user.is_active is False:
            user.is_active = True
            user.save()
        if company.approved is not True:
            company.approved = True
            company.approver = Admin.objects.get(
                id=self.request.session['admin_instance_id'])
            company.approval_date = timezone.now()
            company.save()
        return redirect('admin-company-detail', pk=company.id)


class JobList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = Job.objects.filter(approved=True)
    template_name = 'jobportal/Admin/job_list.html'
    context_object_name = 'job_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class JobListUnapproved(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = Job.objects.filter(Q(approved=None) | Q(approved=False))
    template_name = 'jobportal/Admin/job_list_unapproved.html'
    context_object_name = 'job_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class JobDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Job
    template_name = 'jobportal/Admin/job_detail.html'

    def test_func(self):
        is_admin = self.request.user.user_type == 'admin'
        return is_admin

    def get_context_data(self, **kwargs):
        context = super(JobDetail, self).get_context_data(**kwargs)
        context['prog_list'] = ProgrammeJobRelation.objects.filter(
            job=self.object.id)
        return context


class JobUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    form_class = AdminJobEditForm
    template_name = 'jobportal/Admin/job_update.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_success_url(self):
        return reverse_lazy('admin-job-detail', args=(self.object.id,))

    def get_object(self, queryset=None):
        return get_object_or_404(Job, id=self.kwargs['pk'])


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
        args = dict(minor_list=minor_list, btech_bdes_list=btech_bdes_list,
                    ma_list=ma_list, mtech_mdes_list=mtech_mdes_list,
                    msc_list=msc_list, phd_list=phd_list, jobpk=jobpk,
                    saved_jobrels=saved_jobrels)
        return render(request, self.template_name, args)

    def post(self, request, jobpk):

        job = get_object_or_404(Job, id=jobpk)

        minor_list_ids = request.POST.getlist('selected_minor_ids')
        btech_bdes_list = request.POST.getlist('selected_btech_bdes_ids')
        mtech_mdes_list_ids = request.POST.getlist('selected_mtech_mdes_ids')
        phd_list_ids = request.POST.getlist('selected_phd_ids')
        ma_list_ids = request.POST.getlist('selected_ma_ids')
        msc_list_ids = request.POST.getlist('selected_msc_ids')

        programme_list = Programme.objects.filter(
            Q(id__in=minor_list_ids) |
            Q(id__in=btech_bdes_list) |
            Q(id__in=phd_list_ids) |
            Q(id__in=ma_list_ids) |
            Q(id__in=mtech_mdes_list_ids) |
            Q(id__in=msc_list_ids)
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
    template_name = 'jobportal/Admin/jobrel_list.html'
    context_object_name = 'rel_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_queryset(self):
        return StudentJobRelation.objects.filter(job__id=self.kwargs['pk'])


class StudentList(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Renders a form for searching a student and displays all matching results
    on submission.
    """
    login_url = reverse_lazy('login')
    template = 'jobportal/Admin/student_list.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request):
        form = StudentSearchForm()
        args = dict(form=form)
        return render(request, self.template, args)

    def post(self, request):
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            roll_no = form.cleaned_data['roll_no']
            stud_list = Student.objects.all()
            if name is not None:
                stud_list = stud_list.filter(name__icontains=name)
            if username != '' and username is not None:
                stud_list = stud_list.filter(user__username=username)
            if roll_no is not None:
                stud_list = stud_list.filter(roll_no=roll_no)
            args = dict(form=form, stud_list=stud_list)
            return render(request, self.template, args)
        else:
            return render(request, self.template, dict(form=form))


class StudentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    All details of student.
    """
    login_url = reverse_lazy('login')
    model = Student
    template_name = 'jobportal/Admin/student_detail.html'
    context_object_name = 'student'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_object(self, queryset=None):
        return get_object_or_404(Student, id=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super(StudentDetail, self).get_context_data(**kwargs)
        context['job_list'] = StudentJobRelation.objects.filter(stud__id=
                                                                self.object.id)
        try:
            context['cv'] = CV.objects.get(stud__id=self.object.id)
        except CV.DoesNotExist:
            context['cv'] = None
        try:
            context['avatar'] = Avatar.objects.get(stud__id=self.object.id)
        except Avatar.DoesNotExist:
            context['avatar'] = None
        try:
            context['signature'] = Signature.objects.get(stud__id=
                                                         self.object.id)
        except Signature.DoesNotExist:
            context['signature'] = None

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
    List all events posted by Companies.
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
            job_candidate = form.cleaned_data['job_candidate']
            intern_candidate = form.cleaned_data['intern_candidate']
            csvfile = form.cleaned_data['csv']
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
                            prog=prog,
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
                            stud.minor_prog = minor_prog
                            stud.minor_discipline = minor_discipline
                            stud.save()
                    except IntegrityError:
                        error = 'Student creation failed. IntegrityError'
                    except ValueError:
                        error = 'Student creation failed. ValueError'
                    except TypeError:
                        error = 'Student creation failed. TypeError'
                    userprofile.delete()
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
