import csv
import os
import StringIO
import zipfile

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import update_session_auth_hash
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import (get_object_or_404, get_list_or_404, render,
                              redirect)
from django.utils import timezone
from django.utils.encoding import smart_str
from django.views.generic import (View, TemplateView, FormView, CreateView,
                                  UpdateView, ListView, DetailView)

from .models import (UserProfile, Job, Company, StudentJobRelation,
                     ProgrammeJobRelation, Event, Programme, CV)
from .forms import (CompanyProfileEdit, CompanyJobForm, CompanySignup,
                    EventForm)


class CompanySignUpView(FormView):
    """
    View that handles Company signup and renders the confirmation page.
    """
    form_class = CompanySignup
    template_name = 'jobportal/Company/signup2.html'
    confirm_template = 'jobportal/Company/signupconfirm.html'

    def form_valid(self, form):
        username = form.cleaned_data.pop('username')
        password1 = form.cleaned_data.pop('password1')
        user = UserProfile(username=username,
                           password=make_password(password1),
                           user_type='company', is_active=False)
        user.save()
        company = form.save(commit=False)
        company.user = user
        company.save()
        context = dict(company=company)
        return render(self.request, self.confirm_template, context)


class HomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    View class that handles rendering Home page to Company users.
    """
    login_url = reverse_lazy('login')
    template_name = 'jobportal/Company/home.html'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(user=self.request.user)
        return context


class ProfileDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View class that handles displaying profile to Company users.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    model = Company
    template_name = 'jobportal/Company/profile_detail.html'
    context_object_name = 'company'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_object(self, queryset=None):
        """
        Return Company instance

        ``select_related`` used for fetching ``user`` in one query.
        Check ``select_related`` documentation.
        https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related

        :param queryset: None
        :return: Company instance
        """
        return Company.objects.select_related('user').get(
            id=self.request.session['company_instance_id']
        )


class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View class that renders profile Company profile update form and updates
    the Company instance.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    form_class = CompanyProfileEdit
    template_name = 'jobportal/Company/profile_update.html'
    success_url = reverse_lazy('company-profile-detail')

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Company, id=self.request.session['company_instance_id'])


class PasswordChangeView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View class that renders
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    template_name = 'jobportal/Company/password_update.html'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get(self, request):
        form = PasswordChangeForm(None)
        return render(request, self.template_name, dict(form=form))

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('company-home')
        else:
            return render(request, self.template_name, dict(form=form))


class JobList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    template_name = 'jobportal/Company/job_list.html'
    context_object_name = 'job_list'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_queryset(self):
        return Job.objects.filter(
            company_owner__id=self.request.session['company_instance_id'])

    def get_context_data(self, **kwargs):
        context = super(JobList, self).get_context_data(**kwargs)
        context['present_date'] = timezone.now().date()
        return context


class JobCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    form_class = CompanyJobForm
    template_name = 'jobportal/Company/job_create.html'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def form_valid(self, form):
        job = form.save(commit=False)
        job.posted_by_alumnus = False
        job.posted_by_company = True
        job.company_owner = Company.objects.get(
            id=self.request.session['company_instance_id'])
        return super(JobCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('company-job-detail', args=(self.object.id,))


class JobDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    model = Job
    template_name = 'jobportal/Company/job_detail.html'
    context_object_name = 'job'
    job = None

    def test_func(self):
        is_company = self.request.user.user_type == 'company'
        if not is_company:
            return False
        self.job = get_object_or_404(Job, id=self.kwargs['pk'])
        company_id = self.request.session['company_instance_id']
        if self.job.company_owner.id != company_id:
            return False
        return True

    def get_context_data(self, **kwargs):
        context = super(JobDetail, self).get_context_data(**kwargs)
        context['rel_list'] = ProgrammeJobRelation.objects.filter(
            job=self.object).select_related('prog')
        now = timezone.now()
        context['deadline_over'] = self.job.application_deadline < now
        return context


class JobUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    form_class = CompanyJobForm
    template_name = 'jobportal/Company/job_update.html'
    context_object_name = 'job'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def form_valid(self, form):
        form.save(commit=False)
        return super(JobUpdate, self).form_valid(form)

    def get_object(self, queryset=None):
        job = get_object_or_404(Job, id=self.kwargs['pk'])
        company = Company.objects.get(
            id=self.request.session['company_instance_id'])
        if job.company_owner == company:
            return job
        else:
            return Http404('You are not permitted to view this page')

    def get_success_url(self):
        return reverse_lazy('company-job-detail', args=(self.object.id,))


class JobRelList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    template_name = 'jobportal/Company/jobrel_list.html'
    context_object_name = 'rel_list'
    job = None

    def test_func(self):
        # user is company
        is_company = self.request.user.user_type == 'company'
        if not is_company:
            return False
        self.job = get_object_or_404(Job, id=self.kwargs['pk'])
        company_user = self.request.session['company_instance_id']
        company_owner = self.job.company_owner.id == company_user
        if not company_owner:
            return False
        # deadline has passed
        deadline = self.job.application_deadline
        deadline_over = deadline < timezone.now()
        if not deadline_over:
            return False
        return True

    def get_queryset(self):
        return StudentJobRelation.objects.filter(
            job__id=self.kwargs['pk'], is_debarred=False).order_by(
            'stud__roll_no')

    def get_context_data(self, **kwargs):
        context = super(JobRelList, self).get_context_data(**kwargs)
        context['jobid'] = self.job.id
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
        Tests:
            - User is a Company user
            - User owns the Job whose id is passed
            - Application deadline for the Job has passed
        :return: True if User is allowed else False.
        """
        # user is company
        is_company = self.request.user.user_type == 'company'
        if not is_company:
            return False
        # user is job owner
        job = get_object_or_404(Job, id=self.kwargs['pk'])
        company_user_id = self.request.session['company_instance_id']
        company_owner = job.company_owner.id == company_user_id
        if not company_owner:
            return False
        # deadline has passed
        deadline_passed = job.application_deadline < timezone.now()
        if not deadline_passed:
            return False
        return True

    @staticmethod
    def get(request, pk):
        """
        Returns the CSV containing applicant data.
        CSV Fields:
            1. Roll No
            2. Name
            3. Discipline (Specialization or Branch)
            4. Program
            5. CPI
        :param request: HttpRequest object
        :param pk: id of Job object
        :return: HttpResponse object
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; ' \
                                          'filename="iitg_students_detail.csv"'
        wr = csv.writer(response, quoting=csv.QUOTE_ALL)
        headers = ['Roll No', 'Name', 'Branch/Specialization', 'Programme',
                   'CPI']
        wr.writerow(headers)
        all_studrels = StudentJobRelation.objects.filter(job__id=pk)
        for studrel in all_studrels:
            row = [
                smart_str(studrel.stud.roll_no),
                smart_str(studrel.stud.name),
                smart_str(studrel.stud.discipline),
                smart_str(studrel.stud.prog),
                smart_str(studrel.stud.cpi)
            ]
            wr.writerow(row)
        return response


class EventList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    model = Event
    template_name = 'jobportal/Company/event_list.html'
    context_object_name = 'event_list'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_queryset(self):
        return Event.objects.filter(
            company_owner__id=self.request.session['company_instance_id'])


class EventCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View class that handles rendering EventForm to Company Users and creating
    Event instance on submission.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    form_class = EventForm
    template_name = 'jobportal/Company/event_create.html'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.company_owner = get_object_or_404(
            Company, id=self.request.session['company_instance_id'])
        instance.save()
        return redirect('company-event-detail', pk=instance.id)


class EventDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View class that handles rendering details of Event instance for Company
    users.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    model = Event
    template_name = 'jobportal/Company/event_detail.html'
    context_object_name = 'event'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_object(self, queryset=None):
        event = get_object_or_404(Event, id=self.kwargs['pk'])
        company_id = self.request.session['company_instance_id']
        if event.company_owner.pk == company_id:
            return event
        else:
            return HttpResponseForbidden()


class EventUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    form_class = EventForm
    template_name = 'jobportal/Company/event_update.html'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_object(self, queryset=None):
        return get_object_or_404(Event, id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('company-event-detail', args=(self.object.id,))

    def form_valid(self, form):
        if self.object.is_approved is None:
            form.save()
            return super(EventUpdate, self).form_valid(form)
        else:
            return HttpResponseForbidden()


# TODO: This function is untested
class DownloadStudCV(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    jobrel = None

    def test_func(self):
        is_company = self.request.user.user_type == 'company'
        if not is_company:
            return is_company
        self.jobrel = get_object_or_404(
            StudentJobRelation, id=self.kwargs['pk'])
        company_id = self.request.session['company_instance_id']
        if not self.jobrel.job.company_owner.id == company_id:
            return False
        return True

    def get(self, request, pk, cvno):
        stud_id = self.jobrel.stud.id
        cv = get_object_or_404(CV, stud__id=stud_id)
        if cvno == '1' and bool(cv.cv1.name):
            response = HttpResponse(cv.cv1,
                                    content_type='application/pdf')
            download_name = 'CV_' + str(cv.stud.roll_no) + '_IITG.pdf'
            response['Content-Disposition'] = 'attachment; filename=%s' % \
                                              smart_str(download_name)
            return response
        elif cvno == '2' and bool(cv.cv2.name):
            response = HttpResponse(cv.cv2,
                                    content_type='application/pdf')
            download_name = 'CV_' + str(cv.stud.roll_no) + '_IITG.pdf'
            response['Content-Disposition'] = 'attachment; filename=%s' % \
                                              smart_str(download_name)
            return response
        else:
            raise Http404()


# TODO: This function is untested
class StudJobRelShortlist(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = reverse_lazy('login')

    def test_func(self, **kwargs):
        is_company = self.request.user.user_type == 'company'
        if not is_company:
            return False
        jobrel = get_object_or_404(StudentJobRelation,
                                   id=self.kwargs['jobrelpk'])
        session_id = self.request.session['company_instance_id']
        if jobrel.job.company_owner.id != session_id:
            return False
        return True

    def get(self, request, jobpk, jobrelpk):
        jobrel = get_object_or_404(StudentJobRelation, id=jobrelpk)
        if jobrel.stud.placed:
            msg = 'Student is not available for hiring anymore.'
            level = messages.ERROR
        elif jobrel.shortlist_init:
            msg = 'Student is already shortlisted'
            level = messages.WARNING
        elif jobrel.placed_init and jobrel.placed_approved is None:
            msg = 'Placement Approval is already pending. Candidate cannot ' \
                  'be shortlisted now.'
            level = messages.ERROR
        elif jobrel.placed_init and jobrel.placed_approved is not None:
            msg = 'Placement request has been made already.'
            level = messages.ERROR
        else:
            jobrel.shortlist_init = True
            jobrel.shortlist_init_datetime = timezone.now()
            jobrel.save()
            msg = 'Student has been shortlisted shortlisted.'
            level = messages.SUCCESS

        messages.add_message(request=request, level=level,
                             message=msg, fail_silently=True)
        return redirect('company-jobrel-list', pk=jobpk)


# TODO: This function is untested
class StudJobRelPlace(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')

    def test_func(self, **kwargs):
        # check user type
        is_company = self.request.user.user_type == 'company'
        if not is_company:
            return False
        # check application_deadline
        job = get_object_or_404(Job, id=self.kwargs['jobpk'])
        deadline = job.application_deadline < timezone.now()
        if not deadline:
            return False
        # check job owner
        jobrel = get_object_or_404(StudentJobRelation,
                                   id=self.kwargs['jobrelpk'])
        session_id = self.request.session['company_instance_id']
        if jobrel.job.company_owner.id != session_id:
            return False
        return True

    def get(self, request, jobpk, jobrelpk):
        jobrel = get_object_or_404(StudentJobRelation, id=jobrelpk)
        if jobrel.stud.placed:
            msg = 'Student is not available for hiring anymore.'
            level = messages.ERROR
        elif jobrel.placed_init is True and jobrel.placed_approved is None:
            msg = 'Placement Approval is already pending.'
            level = messages.ERROR
        elif jobrel.placed_init is True and jobrel.placed_approved is not None:
            msg = 'Placement request has been made already.'
            level = messages.ERROR
        else:
            jobrel.placed_init = True
            jobrel.placed_init_datetime = timezone.now()
            jobrel.save()
            msg = 'Placement request has been sent to admin for approval.'
            level = messages.SUCCESS

        messages.add_message(request=request, level=level,
                             message=msg, fail_silently=True)
        return redirect('company-jobrel-list', pk=jobpk)


# TODO: This function is untested
class JobProgrammeCreate(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View that handles creating and validating JobProgrammeRelation instances.
    """
    login_url = reverse_lazy('login')
    raise_exception = False
    template_name = 'jobportal/Company/jobprog_create.html'
    job = None

    def test_func(self):
        is_company = self.request.user.user_type == 'company'
        if not is_company:
            return False
        # get Job instance and related Company instance in one query
        self.job = Job.objects.select_related('company_owner').get(
            id=self.kwargs['jobpk']
        )
        session_id = self.request.session['company_instance_id']
        # check if Company is company_owner of Job instance
        is_owner = self.job.company_owner.id == session_id
        if not is_owner:
            return False
        # check if deadline has passed
        deadline_passed = self.job.application_deadline < timezone.now()
        if deadline_passed:
            return False
        return True

    def get(self, request, jobpk):
        saved_jobrels = [jobrel.prog.id for jobrel in
                         ProgrammeJobRelation.objects.filter(job__id=jobpk)]
        minor_list = Programme.objects.filter(open_for_placement=True,
                                              minor_status=True)
        bachelors_list = Programme.objects.filter(
            open_for_placement=True, minor_status=False).filter(
            Q(name='BTECH') | Q(name='BDES'))

        masters_list = Programme.objects.filter(
            open_for_placement=True, minor_status=False).filter(
            Q(name='MTECH') | Q(name='MDES'))

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
        args = dict(minor_list=minor_list, btech_bdes_list=bachelors_list,
                    ma_list=ma_list, mtech_mdes_list=masters_list,
                    msc_list=msc_list, phd_list=phd_list, jobpk=jobpk,
                    saved_jobrels=saved_jobrels, msr_list=msr_list)
        return render(request, self.template_name, args)

    def post(self, request, jobpk):

        job = get_object_or_404(Job, id=jobpk)

        minor_list_ids = request.POST.getlist('selected_minor_ids')
        btech_bdes_list_ids = request.POST.getlist('selected_btech_bdes_ids')
        mtech_mdes_list_ids = request.POST.getlist('selected_mtech_mdes_ids')
        phd_list_ids = request.POST.getlist('selected_phd_ids')
        ma_list_ids = request.POST.getlist('selected_ma_ids')
        msc_list_ids = request.POST.getlist('selected_msc_ids')
        msr_list_ids = request.POST.getlist('selected_msr_ids')

        programme_list = Programme.objects.filter(
            Q(id__in=minor_list_ids) |
            Q(id__in=btech_bdes_list_ids) |
            Q(id__in=phd_list_ids) |
            Q(id__in=ma_list_ids) |
            Q(id__in=mtech_mdes_list_ids) |
            Q(id__in=msc_list_ids) |
            Q(id__in=msr_list_ids)
        )

        all_programmes = []
        for programme in programme_list:
            all_related_programmes = Programme.objects.filter(
                year_passing=programme.year_passing,
                dept=programme.dept,
                discipline=programme.discipline,
                name=programme.name,
                minor_status=programme.minor_status
            )
            for related_programme in all_related_programmes:
                all_programmes.append(related_programme)

        for programme in all_programmes:
            ProgrammeJobRelation.objects.get_or_create(
                job=job,
                prog=programme
            )
        return redirect('company-job-detail', pk=job.id)


class DownloadBondDocument(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')

    def test_func(self):
        is_company = self.request.user.user_type == 'company'
        if not is_company:
            return False
        return True

    @staticmethod
    def get(request, pk):
        job = get_object_or_404(Job, id=pk)
        response = HttpResponse(job.bond_link, content_type='application/pdf')
        username = job.company_owner.user.username
        download_name = username + '_' + job.designation + '.pdf'
        response['Content-Disposition'] = 'attachment; filename=%s' % \
                                          smart_str(download_name)
        return response
