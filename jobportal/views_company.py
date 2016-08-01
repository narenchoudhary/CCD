import zipfile
import os
import StringIO

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import update_session_auth_hash
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import (get_object_or_404, get_list_or_404, render,
                              redirect)
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import (View, TemplateView, RedirectView, CreateView,
                                  UpdateView, ListView, DetailView, FormView)

from .models import (Job, Company, StudentJobRelation, ProgrammeJobRelation,
                     Alumni, Event, Programme, MinorProgrammeJobRelation)
from .forms import (CompanyProfileEdit, CompanyJobForm, JobProgFormSet,
                    CompanySignup, UserProfileForm, CompanyJobRelForm,
                    EventForm, JobProgMinorFormSet)

from .mixins import CurrentAppMixin

COMPANY_LOGIN_URL = reverse_lazy('login')


# Change password
@login_required(login_url=COMPANY_LOGIN_URL)
def password_change_company(request):

    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("companyhome")
        else:
            args = {'form': form}
            return render(request, 'jobportal/Company/passwordchange.html',
                          args)
    else:
        company_instance = get_object_or_404(
            Company, id=request.session['company_instance_id'])
        form = PasswordChangeForm(request)
        args = {'form': form, 'company_instance': company_instance}
        return render(request, 'jobportal/Company/passwordchange.html', args)


def add_progs(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    formset = JobProgFormSet(request.POST or None, instance=job_instance)

    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect('companyjob', jobid=job_instance.id)
        else:
            args = dict(formset=formset, job_instance=job_instance)
            return render(request, 'jobportal/Company/add_job_progs.html',
                          args)
    else:
        args = dict(formset=formset, job_instance=job_instance)
        return render(request, 'jobportal/Company/add_job_progs.html', args)


class JobProgUpdate(View):

    template = 'jobportal/Company/jobprog_update.html'

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
            return redirect('company-job-detail', pk=job.id)
        else:
            args = dict(formset=formset, job=job)
            return render(request, self.template, args)


class JobProgMinorUpdate(View):

    template = 'jobportal/Company/jobprog_minor_update.html'

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
            return redirect('company-job-detail', pk=job.id)
        else:
            args = dict(formset=formset, job=job)
            return render(request, self.template, args)


@login_required(login_url=COMPANY_LOGIN_URL)
def job_drop(request, jobid):
    # TODO: Check no shortlist bug
    job_instance = get_object_or_404(Job, id=jobid)
    stud_rels = list(StudentJobRelation.objects.get(job=job_instance,
                                                    dropped=False))
    approval_error = False
    for rel in stud_rels:
        if rel.shortlist_init is True and rel.shortlist_approved is not True:
            approval_error = True
            break
        if rel.placed_init is True and rel.placed_approved is not True:
            approval_error = True
            break
    if not approval_error:
        for rel in stud_rels:
            rel.round += 1
            if rel.shortlist_init is False:
                rel.dropped = True
            rel.save()
    # TODO: Message framework
    # TODO: change to render
    return redirect('companycandidates', jobid=job_instance.id)


# Issue: Not working as intended; Most probably it's not using relative path
# SO solution isn't working
# TODO: Debug; Think of some workaround
# TODO: Download CVs as zip
@login_required(login_url=COMPANY_LOGIN_URL)
def download_cvs(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    relation_list = get_list_or_404(StudentJobRelation, job = job_instance)
    filelist = []
    for relation in relation_list:
        if bool(relation.cv1):
            filelist.append(relation.stud.cv1.url)
        if bool(relation.cv2):
            filelist.append(relation.stud.cv2.url)

    zip_subdir = "cvs_for_" + str(job_instance.description)
    zip_filename = "%s.zip" % zip_subdir

    s = StringIO.StringIO()
    zf = zipfile.ZipFile(s, "w")

    for fpath in filelist:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)

    zf.close()

    response = HttpResponse(s.getvalue(),
                            content_type="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return response


class CompanySignUpView(View):

    template = 'jobportal/Company/signup.html'

    def get(self, request):
        userform = UserProfileForm(prefix='user')
        companyform = CompanySignup(prefix='company')
        args = dict(userform=userform, companyform=companyform)
        return render(request, self.template, args)

    def post(self, request):
        companyform = CompanySignup(request.POST, prefix='company')
        userform = UserProfileForm(request.POST, prefix='user')
        if userform.is_valid() and companyform.is_valid():
            user = userform.save()
            user.is_active = False
            user.user_type = 'company'
            user.save()
            company = companyform.save(commit=False)
            company.user = user
            company.save()
            return redirect('signup-confirm')
        else:
            args = dict(userform=userform, companyform=companyform)
            return render(request, self.template, args)


class HomeView(TemplateView):

    template_name = 'jobportal/Company/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(user=self.request.user)
        return context


class ProfileDetail(DetailView):
    model = Company
    template_name = 'jobportal/Company/profile_detail.html'
    context_object_name = 'company'

    def get_object(self, queryset=None):
        return get_object_or_404(Company,
                                 id=self.request.session['company_instance_id'])


class ProfileUpdate(UpdateView):
    form_class = CompanyProfileEdit
    template_name = 'jobportal/Company/profile_update.html'
    success_url = reverse_lazy('company-profile-detail')

    def get_object(self, queryset=None):
        return get_object_or_404(
            Company, id=self.request.session['company_instance_id'])


class PasswordChangeView(CurrentAppMixin, UpdateView):

    form_class = PasswordChangeForm
    success_url = reverse_lazy('company-home')
    template_name = 'jobportal/Company/password_update.html'

    current_app = None
    extra_context = None

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = kwargs.pop('instance')
        return kwargs

    # def form_valid(self, form):
    #     form.save()
    #     messages.add_message(self.request, messages.SUCCESS, 'Password changed successfully.')
    #     return super(PasswordChangeView, self).form_valid(form)

    @method_decorator
    def dispatch(self, request, *args, **kwargs):
        super(PasswordChangeView, self).dispatch(*args, **kwargs)


class JobList(ListView):
    template_name = 'jobportal/Company/job_list.html'
    context_object_name = 'job_list'

    def get_queryset(self):
        return Job.objects.filter(
            company_owner__id=self.request.session['company_instance_id'])


class JobCreate(CreateView):
    form_class = CompanyJobForm
    template_name = 'jobportal/Company/job_create.html'

    def form_valid(self, form):
        job = form.save(commit=False)
        job.posted_by_alumnus = False
        job.posted_by_company = True
        job.company_owner = Company.objects.get(
            id=self.request.session['company_instance_id'])
        return super(JobCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('company-job-detail', args=(self.object.id,))


class JobDetail(DetailView):
    model = Job
    template_name = 'jobportal/Company/job_detail.html'
    context_object_name = 'job'

    def get_object(self, queryset=None):
        job = get_object_or_404(Job, id=self.kwargs['pk'])
        company = get_object_or_404(
            Company, id=self.request.session['company_instance_id'])
        if job.company_owner == company:
            return job
        else:
            return Http404('You are not permitted to vie this page')

    def get_context_data(self, **kwargs):
        context = super(JobDetail, self).get_context_data(**kwargs)
        context['rel_list'] = ProgrammeJobRelation.objects.filter(
            job=self.object.id)
        context['rel_minor_list'] = MinorProgrammeJobRelation.objects.filter(
            job=self.object.id)
        return context


class JobUpdate(UpdateView):
    form_class = CompanyJobForm
    template_name = 'jobportal/Company/job_update.html'
    context_object_name = 'job'

    def form_valid(self, form):
        job = form.save(commit=False)
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


class JobDelete(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    raise_exception = True

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get(self, request, pk):
        job = Job.objects.get(id=pk)
        if job.company_owner.id == request.session['company_instance_id']:
            job.is_deleted = True
            job.save()
            return redirect('company-job-list')
        else:
            return Http404()


class JobRelList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    raise_exception = True
    template_name = 'jobportal/Company/jobrel_list.html'
    context_object_name = 'rel_list'
    job = None

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_queryset(self):
        self.job = Job.objects.get(id=self.kwargs['pk'])
        owner_id = self.job.company_owner.id
        user_id = self.request.session['company_instance_id']
        if owner_id == user_id and self.job.approved:
            return StudentJobRelation.objects.filter(job__id=self.kwargs['pk'])
        else:
            return Http404()

    def get_context_data(self, **kwargs):
        context = super(JobRelList, self).get_context_data(**kwargs)
        context['jobid'] = self.job.id
        deadline = self.job.application_deadline
        context['hide'] = timezone.now().date() <= deadline
        return context


class JobRelUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    form_class = CompanyJobRelForm
    template_name = 'jobportal/Company/jobrel_update.html'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_object(self, queryset=None):
        return get_object_or_404(StudentJobRelation, id=self.kwargs['pk'])

    def form_valid(self, form):
        form.save()
        stud_name = self.object.stud.first_name + \
                    self.object.stud.middle_name + self.object.stud.last_name
        msg = 'Status of ' + stud_name + " has been updated successfully."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return redirect('company-jobrel-list', pk=self.kwargs['jobpk'])

    def get_success_url(self):
        return reverse_lazy('company-jobrel-update', args=(self.object.id,))


class JobRelUpdateRound(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    raise_exception = True
    template_name = 'jobportal/Company/jobrel_list.html'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get(self, request, pk):
        job = get_object_or_404(Job, id=pk)
        if job.company_owner.id == request.session['company_instance_id']:
            rel_list = StudentJobRelation.objects.filter(job__id=pk)
            # check if jobrel approval is pending
            if self.get_rel_status(rel_list):
                # change status of jobrels
                rel_list = self.change_rel_status(rel_list)
            else:
                # message to inform pending approvals
                messages.add_message(request, messages.ERROR,
                                     'Some approvals are pending.')
            # return render(request, self.template_name, dict(rel_list=rel_list, jobid=job.id))
            return redirect('company-jobrel-list', pk=job.id)
        else:
            return Http404()

    @staticmethod
    def get_rel_status(jobrel_list):
        status = True
        for rel in jobrel_list:
            if rel.shortlist_init is True and rel.shortlist_approved is None:
                status = False
                break
            elif rel.placed_init is True and rel.placed_approved is None:
                status = False
                break
        return status

    @staticmethod
    def change_rel_status(jobrel_list):
        for rel in jobrel_list:
            # unshortlisted or shortlist+rejected => dropped
            if rel.shortlist_init is False and rel.shortlist_approved is not True:
                rel.dropped = True
                rel.save()
            # shortlist+approved => unshortlisted+unapproved
            elif rel.shortlist_init is True and rel.shortlist_approved is True:
                rel.shortlist_init = False
                rel.shortlist_approved = None
                rel.round += 1
                rel.save()
        return rel


class ProgrammeList(View):
    template_name = 'jobportal/Company/programme_list.html'

    def get(self, request):
        prog_minor_list = Programme.objects.filter(open_for_placement=True,
                                                   minor_status=True)
        prog_major_list = Programme.objects.filter(open_for_placement=True,
                                                   minor_status=False)
        args = dict(prog_major_list=prog_major_list,
                    prog_minor_list=prog_minor_list)
        return render(request, self.template_name, args)


class EventList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Event
    template_name = 'jobportal/Company/event_list.html'
    context_object_name = 'event_list'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_queryset(self):
        return Event.objects.filter(
            company_owner__id=self.request.session['company_instance_id'])


class EventCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    form_class = EventForm
    template_name = 'jobportal/Company/event_create.html'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_success_url(self):
        return reverse_lazy('company-event-detail', args=(self.object.id,))

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.company_owner = get_object_or_404(
            Company, id=self.request.session['company_instance_id'])
        instance.save()
        return super(EventCreate, self).form_valid(form)


class EventDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Event
    template_name = 'jobportal/Company/event_detail.html'
    context_object_name = 'event'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_object(self, queryset=None):
        event = get_object_or_404(Event, id=self.kwargs['pk'])
        if event.company_owner.pk is self.request.session['company_instance_id']:
            return event
        else:
            # HTTP ERROR 403
            return HttpResponseForbidden()
