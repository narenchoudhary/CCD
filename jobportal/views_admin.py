from django.contrib import messages
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
                     ProgrammeJobRelation, UserProfile,
                     MinorProgrammeJobRelation, Event)
from .forms import (AddCompany, AdminJobEditForm, AddStudent, JobProgFormSet,
                    AdminJobRelForm, StudentSearchForm, EditCompany,
                    JobProgMinorFormSet, ProgrammeForm, AdminEventForm)

from internships.models import IndInternship, StudentInternRelation


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


class AdminManage(TemplateView):

    template_name = 'jobportal/Admin/manage.html'


class YearList(ListView):
    queryset = Year.objects.all()
    template_name = 'jobportal/Admin/year_list.html'
    context_object_name = 'years'


class YearCreate(CreateView):
    model = Year
    fields = '__all__'
    template_name = 'jobportal/Admin/year_create.html'
    success_url = reverse_lazy('year-list')


class YearDelete(DeleteView):
    model = Year
    success_url = reverse_lazy('year-list')


class DepartmentList(ListView):
    queryset = Department.objects.all()
    template_name = 'jobportal/Admin/department_list.html'
    context_object_name = 'departments'


class DepartmentDetail(DetailView):
    model = Department
    template_name = 'jobportal/Admin/department_detail.html'


class DepartmentCreate(CreateView):
    model = Department
    fields = '__all__'
    template_name = 'jobportal/Admin/department_create.html'
    success_url = reverse_lazy('department-list')


class DepartmentUpdate(UpdateView):
    model = Department
    fields = '__all__'
    template_name = 'jobportal/Admin/department_update.html'
    success_url = reverse_lazy('department-list')

    def get_object(self, queryset=None):
        obj = Department.objects.get(id=self.kwargs['pk'])
        return obj


class DepartmentDelete(DeleteView):
    model = Department
    success_url = reverse_lazy('department-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProgrammeList(ListView):
    queryset = Programme.objects.all()
    template_name = 'jobportal/Admin/programme_list.html'
    context_object_name = 'programme_list'


class ProgrammeCreate(CreateView):
    form_class = ProgrammeForm
    template_name = 'jobportal/Admin/programme_create.html'
    success_url = reverse_lazy('programme-list')


class ProgrammeUpdate(UpdateView):
    model = Programme
    fields = '__all__'
    template_name = 'jobportal/Admin/programme_update.html'
    success_url = reverse_lazy('programme-list')

    def get_object(self, queryset=None):
        return Programme.objects.get(id=self.kwargs['pk'])


class ProgrammeDelete(DeleteView):
    model = Programme
    success_url = reverse_lazy('programme-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProgrammePlacementList(ListView):
    template_name = 'jobportal/Admin/programme_placement_list.html'
    context_object_name = 'programme_list'

    def get_queryset(self):
        return Programme.objects.filter(open_for_placement=True)


class ProgrammeInternshipList(ListView):

    template_name = 'jobportal/Admin/programme_internship_list.html'
    context_object_name = 'programme_list'

    def get_queryset(self):
        return Programme.objects.filter(open_for_internship=True)


class ProgrammePlacementDelete(View):

    def get(self, request, pk):
        prog = get_object_or_404(Programme, id=pk)
        if prog.open_for_placement:
            prog.open_for_placement = False
            prog.save()
        return redirect('admin-programme-placement-list')


class ProgrammeInternshipDelete(View):

    def get(self, request, pk):
        prog = get_object_or_404(Programme, id=pk)
        if prog.open_for_internship:
            prog.open_for_internship = False
            prog.save()
        return redirect('admin-programme-internship-list')


class CompanySignupList(ListView):
    queryset = Company.objects.filter(approved=None)
    template_name = 'jobportal/Admin/company_signup_list.html'
    context_object_name = 'company_list'


class CompanyList(ListView):
    queryset = Company.objects.filter(approved=True)
    template_name = 'jobportal/Admin/company_list.html'
    context_object_name = 'company_list'


class CompanyCreate(CreateView):
    form = AddCompany
    template_name = 'jobportal/Admin/company_create.html'
    success_url = reverse_lazy('company-detail')


class CompanyDetail(DetailView):
    model = Company
    template_name = 'jobportal/Admin/company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetail, self).get_context_data(**kwargs)
        company_instance = Company.objects.get(id=self.kwargs['pk'])
        context['company'] = company_instance
        context['intern_list'] = IndInternship.objects.filter(company_owner=
                                                              company_instance)
        context['job_list'] = Job.objects.filter(company_owner=
                                                 company_instance)
        return context


class CompanyUpdate(UpdateView):
    form_class = EditCompany
    template_name = 'jobportal/Admin/company_update.html'

    def get_object(self, queryset=None):
        return Company.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('admin-company-detail', args=(self.object.id,))


class CompanyApprove(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = reverse_lazy('login')
    raise_exception = True

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


class CompanyDelete(View):

    url = reverse_lazy('admin-company-list')

    def get(self, request, pk):
        company = get_object_or_404(Company, id=pk)
        company.is_deleted = True
        company.deletion_date = timezone.now()
        company.save()
        return redirect('admin-company-detail', pk=pk)


class JobList(ListView):
    queryset = Job.objects.filter(approved=True)
    template_name = 'jobportal/Admin/job_list.html'
    context_object_name = 'job_list'


class JobListUnapproved(ListView):
    queryset = Job.objects.filter(approved=None)
    template_name = 'jobportal/Admin/job_list_unapproved.html'
    context_object_name = 'job_list'


class JobDetail(DetailView):
    model = Job
    template_name = 'jobportal/Admin/job_detail.html'

    def get_context_data(self, **kwargs):
        context = super(JobDetail, self).get_context_data(**kwargs)
        context['prog_list'] = ProgrammeJobRelation.objects.filter(
            job=self.object.id)
        context['prog_minor_list'] = MinorProgrammeJobRelation.objects.filter(
            job=self.object.id)
        return context


class JobUpdate(UpdateView):
    form_class = AdminJobEditForm
    template_name = 'jobportal/Admin/job_update.html'

    def get_success_url(self):
        return reverse_lazy('admin-job-detail', args=(self.object.id,))

    def get_object(self, queryset=None):
        return get_object_or_404(Job, id=self.kwargs['pk'])


class JobApprove(View):

    def get(self, request, pk):
        job = get_object_or_404(Job, id=pk)
        if job.approved is not True:
            job.approved = True
            job.approved_on = timezone.now()
            job.save()
        return redirect('admin-job-detail', pk=pk)


class JobRelList(ListView):
    template_name = 'jobportal/Admin/jobrel_list.html'
    context_object_name = 'rel_list'

    def get_queryset(self):
        return StudentJobRelation.objects.filter(job__id=self.kwargs['pk'])


class JobRelUpdate(UpdateView):
    form_class = AdminJobRelForm
    template_name = 'jobportal/Admin/jobrel_update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(StudentJobRelation, id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('admin-jobrel-update', args=(self.object.id,))


class StudentList(View):

    template = 'jobportal/Admin/student_list.html'

    def get(self, request):
        form = StudentSearchForm()
        args = dict(form=form)
        return render(request, self.template, args)

    def post(self, request):
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            dept_code = form.cleaned_data['dept_code']
            dept_code = dept_code.upper()
            programme = form.cleaned_data['programme']
            minor_status = form.cleaned_data['minor_status']
            try:
                prog = Programme.objects.get(year__current_year=year,
                                             dept__dept_code=dept_code,
                                             name=programme,
                                             minor_status=minor_status)
                stud_list = Student.objects.filter(prog=prog)
                args = dict(form=form, stud_list=stud_list)
                return render(request, self.template, args)
            except Programme.DoesNotExist:
                messages.error(request, 'No such programe exists.')
                return render(request, self.template, dict(form=form))
        else:
            return render(request, self.template, dict(form=form))


class StudentDetail(DetailView):
    model = Student
    template_name = 'jobportal/Admin/student_detail.html'
    context_object_name = 'student'

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
    raise_exception = True
    context_object_name = 'rel_list'
    template_name = 'jobportal/Admin/jobrel_list_unapproved.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_queryset(self):
        return StudentJobRelation.objects.filter(
            Q(placed_approved__isnull=True))


class JobProgUpdate(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = reverse_lazy('login')
    raise_exception = True
    template = 'jobportal/Admin/jobprog_update.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request, pk):
        job = get_object_or_404(Job, id=pk)
        formset = JobProgFormSet(instance=job)
        args = dict(formset=formset, job=job)
        return render(request, self.template, args)

    def post(self, request, pk):
        job = get_object_or_404(Job, id=pk)
        formset = JobProgFormSet(request.POST, instance=job)
        if formset.is_valid():
            formset.save()
            return redirect('admin-job-detail', pk=job.id)
        else:
            args = dict(formset=formset, job=job)
            return render(request, self.template, args)


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


class JobProgMinorUpdate(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = reverse_lazy('login')
    raise_exception = True
    template = 'jobportal/Admin/jobprog_minor_update.html'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get(self, request, pk):
        job = get_object_or_404(Job, id=pk)
        formset = JobProgMinorFormSet(instance=job)
        args = dict(formset=formset, job=job)
        return render(request, self.template, args)

    def post(self, request, pk):
        job = get_object_or_404(Job, id=pk)
        formset = JobProgMinorFormSet(request.POST, instance=job)
        if formset.is_valid():
            formset.save()
            return redirect('admin-job-detail', pk=job.id)
        else:
            args = dict(formset=formset, job=job)
            return render(request, self.template, args)


class EventList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Event
    template_name = 'jobportal/Admin/event_list.html'
    context_object_name = 'event_list'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_queryset(self):
        return Event.objects.all().order_by('-creation_datetime')


class EventDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Event
    template_name = 'jobportal/Admin/event_detail.html'
    context_object_name = 'event'

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def get_object(self, queryset=None):
        return get_object_or_404(Event, id=self.kwargs['pk'])


class EventUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    raise_exception = True
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
