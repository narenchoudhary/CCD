import csv
import codecs
import string
import random

from sqlite3.dbapi2 import IntegrityError

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import (View, ListView, CreateView, DetailView,
                                  TemplateView, UpdateView, DeleteView,
                                  RedirectView, FormView)

from .models import (Admin, Student, Company, Job, StudentJobRelation, CV,
                     Avatar, Signature, Department, Year, Programme,
                     ProgrammeJobRelation, UserProfile, Event)
from .forms import (AdminJobEditForm, StudentSearchForm,
                    EditCompany, ProgrammeForm, AdminEventForm,
                    StudentProfileUploadForm, StudentFeeCSVForm)
from .constants import CATEGORY


class HomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    login_url = reverse_lazy('login')
    raise_exception = True
    template_name = 'jobportal/Admin/home.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['admin'] = Admin.objects.get(user=self.request.user)
        return context


class YearList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = Year.objects.all()
    template_name = 'jobportal/Admin/year_list.html'
    context_object_name = 'years'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class YearCreate(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Year
    fields = '__all__'
    template_name = 'jobportal/Admin/year_create.html'
    success_url = reverse_lazy('year-list')

    def test_func(self):
        return self.request.user.user_type == 'admin'


class DepartmentList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = Department.objects.all()
    template_name = 'jobportal/Admin/department_list.html'
    context_object_name = 'departments'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class DepartmentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Department
    template_name = 'jobportal/Admin/department_detail.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class DepartmentCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Department
    fields = '__all__'
    template_name = 'jobportal/Admin/department_create.html'
    success_url = reverse_lazy('department-list')

    def test_func(self):
        return self.request.user.user_type == 'admin'


class DepartmentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Department
    fields = '__all__'
    template_name = 'jobportal/Admin/department_update.html'
    success_url = reverse_lazy('department-list')

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_object(self, queryset=None):
        obj = Department.objects.get(id=self.kwargs['pk'])
        return obj


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


class CompanyUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    form_class = EditCompany
    template_name = 'jobportal/Admin/company_update.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_object(self, queryset=None):
        return Company.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('admin-company-detail', args=(self.object.id,))


class CompanyApprove(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request, pk):
        company = Company.objects.get(id=pk)
        user = company.user
        print company
        print company.user
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
    queryset = Job.objects.filter(approved=None)
    template_name = 'jobportal/Admin/job_list_unapproved.html'
    context_object_name = 'job_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'


class JobDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Job
    template_name = 'jobportal/Admin/job_detail.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

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
    login_url = reverse_lazy('login')
    template_name = 'jobportal/Admin/jobrel_list.html'
    context_object_name = 'rel_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_queryset(self):
        return StudentJobRelation.objects.filter(job__id=self.kwargs['pk'])


class StudentList(LoginRequiredMixin, UserPassesTestMixin, View):
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
                print("name")
                stud_list = stud_list.filter(name__icontains=name)
            if username != '' and username is not None:
                print("username")
                stud_list = stud_list.filter(user__username=username)
            if roll_no is not None:
                print("roll")
                stud_list = stud_list.filter(roll_no=roll_no)
            args = dict(form=form, stud_list=stud_list)
            return render(request, self.template, args)
        else:
            return render(request, self.template, dict(form=form))


class StudentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
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
    login_url = reverse_lazy('login')
    context_object_name = 'rel_list'
    template_name = 'jobportal/Admin/jobrel_list_unapproved.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_queryset(self):
        return StudentJobRelation.objects.filter(
            Q(placed_approved__isnull=True))


class StudJobRelPlaceApprove(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = reverse_lazy('login')
    raise_exception = True

    def test_func(self):
        is_admin = self.request.user.user_type == 'admin'
        if not is_admin:
            return True
        job = get_object_or_404(Job, id=self.kwargs['jobpk'])
        deadline_ok = job.application_deadline < timezone.now().date()
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
    login_url = reverse_lazy('login')
    template_name = 'jobportal/Admin/student_create.html'
    col_count = 13
    password_len = 8
    # form_class = StudentUploadForm

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def validate_csv_row(self, row):
        # CSV format
        # Col0: Webmail: no checking
        # Col1: Roll No: Must be number
        # Col2: Name: no checking
        # Col3: Year: Must be in Db
        # Col4: Dept: Must be in Db
        # Col5: Prog: Must be in Db
        # Col6: Minor Year: Must be in Db
        # Col7: Minor Dept: Must be in Db
        # Col8: Minor Prog: Must be in Db
        # Col9: Category: Must be in constants.CATEGORY
        # Col10: CPI: Must be Float
        # Col11: Nationality: NO checking
        # Col12: Gender: Must be in [M, F]
        num_cols = len(row)
        if self.col_count != num_cols:
            return False, 'Total number of columns is not ' + str(
                self.col_count)
        try:
            roll_no = int(row[1])
        except ValueError:
            return False, 'Roll number is not a valid number'
        try:
            year = int(row[3])
        except ValueError:
            return False, 'Year is not a valid number.'
        try:
            year_instance = Year.objects.get(current_year=year)
        except Year.DoesNotExist:
            return False, 'Year %s doen not exist in DB' % year
        try:
            dept_code = str(row[4]).upper()
            dept_instance = Department.objects.get(year=year_instance,
                                                   dept_code=dept_code)
        except Department.DoesNotExist:
            return False, 'Department %s does not not exist in DB' \
                   % str(row[4]).upper()
        try:
            prog = str(row[5]).upper()
            Programme.objects.get(year=year_instance, dept=dept_instance,
                                  name=prog, minor_status=False)
        except Programme.DoesNotExist:
            return False, 'Programme %s does not exist in DB' \
                   % str(row[5]).upper()
        if row[6] != '':
            try:
                year_instance = Year.objects.get(current_year=year)
            except Year.DoesNotExist:
                return False, 'Minor year %s doen not exist in DB' % year
        if row[7] != '':
            try:
                dept_code = str(row[7]).upper()
                dept_instance = Department.objects.get(year=year_instance,
                                                       dept_code=dept_code)
            except Department.DoesNotExist:
                return False, 'Department %s does not not exist in DB' \
                       % dept_code
        if row[8] != '':
            try:
                prog = str(row[8]).upper()
                Programme.objects.get(year=year_instance, dept=dept_instance,
                                      name=prog, minor_status=True)
            except Programme.DoesNotExist:
                return False, 'Programme %s does not exist in DB' \
                       % prog
        category = str(row[9])
        if category not in [cat[0] for cat in CATEGORY]:
            return False, 'Invalid Category'

        try:
            cpi = float(row[10])
        except ValueError:
            return False, 'CPI not a valid number.'

        if row[12] not in ['M', 'F']:
            return False, 'Gender must be M or F only.'

        return True, None

    def get(self, request):
        form = StudentProfileUploadForm()
        return render(request, self.template_name, dict(form=form))

    # TODO: Add Transaction
    def post(self, request):
        form = StudentProfileUploadForm(request.POST, request.FILES)
        print("form ready")
        if form.is_valid():
            csvfile = form.cleaned_data['csv']
            reader = csv.reader(csvfile, delimiter=',')
            error_rows = []
            error_msg = []
            rowcount = 0
            for row in reader:
                rowcount += 1
                row_ok, error = self.validate_csv_row(row)
                if not row_ok:
                    error_rows.append(rowcount)
                    error_msg.append(error)
                    continue
                username = row[0]
                # dummy password
                password = ''.join(
                    random.SystemRandom().choice(
                        string.ascii_uppercase + string.digits)
                    for _ in range(self.password_len))
                try:
                    userprofile = UserProfile.objects.get(
                        username=username, user_type='student'
                    )
                except UserProfile.DoesNotExist:
                    userprofile = UserProfile.objects.create(
                        username=username,
                        password=make_password(password=username),
                        is_active=False,
                        user_type='student'
                    )
                    try:
                        year = Year.objects.get(current_year=int(row[3]))
                        dept = Department.objects.get(
                            year=year, dept_code=str(row[4]).upper())
                        prog = Programme.objects.get(
                            year=year, dept=dept, name=str(row[5]),
                            minor_status=False)
                        minor_year = Year.objects.get(current_year=int(row[6]))
                        minor_dept = Department.objects.get(
                            year=minor_year, dept_code=str(row[7]).upper())
                        minor_prog = Programme.objects.get(
                            year=minor_year, dept=minor_dept, name=str(row[8]),
                            minor_status=True)
                        stud = Student.objects.create(
                            user=userprofile,
                            iitg_webmail=str(username) + '@iitg.ac.in',
                            roll_no=int(row[1]),
                            name=row[2],
                            year=year,
                            dept=dept,
                            prog=prog,
                            minor_year=minor_year,
                            minor_dept=minor_dept,
                            minor_prog=minor_prog,
                            category=str(row[6]).upper(),
                            cpi=float(row[10]),
                            nationality=str(row[11]),
                            sex=str(row[12]).upper(),
                        )
                    except ValueError or TypeError or IntegrityError:
                        userprofile.delete()
                        error_rows.append(rowcount)
                        error = 'Student creation failed. Integrity Error'
                        error_msg.append(error)
            zipped_data = zip(error_rows, error_msg)
            args = dict(zipped_data=zipped_data, form=form)
            return render(request, self.template_name, args)
        else:
            return render(request, self.template_name, dict(form=form))


class StudentFeeStatusView(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = reverse_lazy('login')
    raise_exception = True
    template_name = 'jobportal/Admin/student_fee_update.html'
    col_count = 2

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request):
        form = StudentFeeCSVForm(None)
        return render(request, self.template_name, dict(form=form))

    def validate_csv_row(self, row):
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
            print("reader init done")
            error_rows = []
            error_msg = []
            rowcount = 0
            for row in reader:
                rowcount += 1
                print(row)
                row_ok, error = self.validate_csv_row(row)
                print("row ok " + str(row_ok))
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
