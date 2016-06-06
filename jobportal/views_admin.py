from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (View, ListView, CreateView, DetailView, TemplateView,
                                  UpdateView, DeleteView, RedirectView)

from .models import (Admin, Student, Job, StudentJobRelation, Company, Department, Year,
                     Programme, ProgrammeJobRelation, UserProfile)
from .forms import (AddCompany, AddEditDepartment, AddEditProgramme, AddEditYear, AdminJobEditForm,
                    AddStudent, JobProgFormSet, EditStudentAdmin, StudentSearchForm, EditCompany)
from internships.models import IndInternship, StudentInternRelation

ADMIN_LOGIN_URL = reverse_lazy('login')


def edit_progs(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    formset = JobProgFormSet(request.POST or None, instance=job_instance)
    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect('review_job', jobid=job_instance.id)
        else:
            args = dict(formset=formset, job_instance=job_instance)
            return render(request, 'jobportal/Admin/edit_progs_formset.html', args)
    else:
        args = dict(formset=formset, job_instance=job_instance)
        return render(request, 'jobportal/Admin/edit_progs_formset.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def approve_job(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    job_instance.approved = True
    job_instance.approved_on = datetime.now()
    job_instance.save()
    return redirect('review_job', jobid=job_instance.id)


@login_required(login_url=ADMIN_LOGIN_URL)
def sent_back_job(jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    job_instance.sent_back = True
    job_instance.save()
    return redirect('review_job', jobid=job_instance.id)


@login_required(login_url=ADMIN_LOGIN_URL)
def admin_manage(request):
    return render(request, 'jobportal/Admin/manage.html')


@login_required(login_url=ADMIN_LOGIN_URL)
def add_student(request):
    add_student_form = AddStudent(request.POST or None)
    if request.method == "POST":
        if add_student_form.is_valid():
            username = add_student_form.cleaned_data['username']
            password = add_student_form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user_profile_instance = UserProfile.objects.create(user=user, login_type="Current Student")
            student_instance = add_student_form.save(commit=False)
            student_instance.user = user_profile_instance
            student_instance.save()
            args = dict(created='Student', webmail=username)
            return render(request, 'jobportal/Admin/manage.html', args)
        else:
            args = dict(add_student_form=add_student_form)
            return render(request, 'jobportal/Admin/add_student.html', args)
    else:
        args = dict(add_student_form=add_student_form)
        return render(request, 'jobportal/Admin/add_student.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def search_students(request):
    studentsearch_form = StudentSearchForm(request.POST or None)
    if request.method == "POST":
        if studentsearch_form.is_valid():
            student_programme = studentsearch_form.cleaned_data['programme']
            student_year = studentsearch_form.cleaned_data['year']
            student_departent = studentsearch_form.cleaned_data['department']
            students_list = Student.objects.all().filter(
                prog__name=student_programme).filter(
                dept__dept_code=student_departent).filter(
                year__current_year=student_year)

            args = dict(students_list=students_list, student_search_form=studentsearch_form)
            return render(request, 'jobportal/Admin/all_users.html', args)
        else:
            args = dict(student_search_form=studentsearch_form)
            return render(request, 'jobportal/Admin/all_users.html', args)
    else:
        args = dict(student_search_form=studentsearch_form)
        return render(request, 'jobportal/Admin/all_users.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def review_stud_profile(request, studid):
    student_instance = get_object_or_404(Student, id=studid)
    args = dict(edited='Student', student_instance=student_instance)
    return render(request, 'jobportal/Admin/review_profile.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def edit_student(request, studid):
    student_instance = get_object_or_404(Student, id=studid)
    edit_student_form = EditStudentAdmin(request.POST or None, instance=student_instance)
    if request.method == "POST":
        if edit_student_form.is_valid():
            edit_student_form.save()
            return redirect('review_stud_profile', studid=studid)
        else:
            args = dict(student_profile_edit_form=edit_student_form, studid=studid)
            return render(request, 'jobportal/Admin/edit_student_profile.html', args)
    else:
        args = dict(student_profile_edit_form=edit_student_form, studid=studid)
        return render(request, 'jobportal/Admin/edit_student_profile.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def job_candidates(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    relation_list_stud = StudentJobRelation.objects.all().filter(job=job_instance)
    args = dict(relation_list_stud=relation_list_stud, job_instance=job_instance)
    return render(request, 'jobportal/Admin/job_candidates.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def approve_action(request, applicant_type, relationid):
    if applicant_type == "stud":
        relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    else:
        relation_instance = None
    args = dict(relation_instance=relation_instance, applicant_type=applicant_type)
    return render(request, 'jobportal/Admin/approve_actions.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def approve_stud_relation(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)

    if relation_instance.placed_init is True:
        if relation_instance.placed_approved is not True:
            relation_instance.placed_approved = True
            relation_instance.save()

    if relation_instance.shortlist_init is True:
        if relation_instance.shortlist_approved is not True:
            relation_instance.shortlist_approved = True
            relation_instance.save()
    return redirect("approve_action", applicant_type="stud", relationid=relationid)


@login_required(login_url=ADMIN_LOGIN_URL)
def admin_approvals(request, object_type):
    if str(object_type) == "job":
        job_list = Job.objects.all().filter(approved__isnull=True)
        intern_list = IndInternship.objects.all().filter(approved__isnull=True)
        args = dict(intern_list=intern_list, job_list=job_list)
        return render(request, 'jobportal/Admin/unapprv_job.html', args)
    elif str(object_type) == "job_progress":
        # job_shortlist = StudentJobRelation.objects.all().filter(
        #     shortlist_init=True, shortlist_approved__isnull=True
        # )
        # job_place_list = StudentJobRelation.objects.all().filter(
        #     placed_init=True, placed_approved__isnull=True
        # )
        intern_shortlist = StudentInternRelation.objects.all().filter(
            shortlist_init=True, shortlist_approved__isnull=True
        )
        intern_hire = StudentInternRelation.objects.all().filter(
            intern_init=True, intern_approved__isnull=True
        )
        intern_ppo = StudentInternRelation.objects.all().filter(
            ppo_init=True, ppo_approved__isnull=True
        )
        args = dict(intern_hire=intern_hire, intern_ppo=intern_ppo, intern_shortlist=intern_shortlist)
        return render(request, 'jobportal/Admin/unapprv_progress.html', args)
    else:
        return redirect("admin-home")


class HomeView(TemplateView):

    template_name = 'jobportal/Admin/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['admin'] = Admin.objects.get(user=self.request.user)
        return context


class YearList(ListView):
    queryset = Year.objects.all()
    template_name = 'jobportal/Admin/year_list.html'
    context_object_name = 'years'


class YearCreate(CreateView):
    form_class = AddEditYear
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
    form_class = AddEditDepartment
    template_name = 'jobportal/Admin/department_create.html'
    success_url = reverse_lazy('department-list')


class DepartmentUpdate(UpdateView):
    form_class = AddEditDepartment
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
    form_class = AddEditProgramme
    template_name = 'jobportal/Admin/programme_create.html'
    success_url = reverse_lazy('programme-list')


class ProgrammeUpdate(UpdateView):
    form_class = AddEditProgramme
    template_name = 'jobportal/Admin/programme_update.html'
    success_url = reverse_lazy('programme-list')

    def get_object(self, queryset=None):
        return Programme.objects.get(id=self.kwargs['pk'])


class ProgrammeDelete(DeleteView):
    model = Programme
    success_url = reverse_lazy('programme-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CompanyList(ListView):
    queryset = Company.objects.all()
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
        context['intern_list'] = IndInternship.objects.filter(company_owner=company_instance)
        context['job_list'] = Job.objects.filter(company_owner=company_instance)
        return context


class CompanyUpdate(UpdateView):
    form_class = EditCompany
    template_name = 'jobportal/Admin/company_update.html'

    def get_object(self, queryset=None):
        return Company.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('admin-company-detail', args=(self.object.id,))


class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('company-list')


class JobList(ListView):
    queryset = Job.objects.all()
    template_name = 'jobportal/Admin/job_list.html'
    context_object_name = 'job_list'


class JobDetail(DetailView):
    model = Job
    template_name = 'jobportal/Admin/job_detail.html'


class JobUpdate(UpdateView):
    form_class = AdminJobEditForm
    template_name = 'jobportal/Admin/job_update.html'

    def get_success_url(self):
        return reverse_lazy('admin-job-detail', args=(self.object.id,))

    def get_object(self, queryset=None):
        return get_object_or_404(Job, id=self.kwargs['pk'])


class CompanySignupList(ListView):
    queryset = Company.objects.filter(approved=False)
    template_name = 'jobportal/Admin/company_signup_list.html'
    context_object_name = 'company_list'


class CompanyApproveView(View):

    def get(self, request, pk):
        company = Company.objects.get(id=pk)
        user = company.user
        if user is not None and user.is_active is False:
            user.is_active = True
            user.save()
        company.approved = True
        company.save()
        return redirect('admin-company-detail', pk=company.id)
