from datetime import datetime, timedelta
import zipfile
import os
import StringIO

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import (View, TemplateView, RedirectView, CreateView,
                                  UpdateView, ListView, DetailView, FormView)

from alumnijobs.models import AlumJobRelation

from .models import Student, Job, Company, StudentJobRelation, ProgrammeJobRelation, Alumni, Event
from .forms import (CompanyProfileEdit, CompanyJobForm, JobProgFormSet, CompanySignup,
                    UserProfileForm, CustomPasswordChangeForm)
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
            return render(request, 'jobportal/Company/passwordchange.html', args)
    else:
        company_instance = get_object_or_404(Company, id=request.session['company_instance_id'])
        form = PasswordChangeForm(request)
        args = {'form': form, 'company_instance': company_instance}
        return render(request, 'jobportal/Company/passwordchange.html', args)


@login_required(login_url=COMPANY_LOGIN_URL)
def company_add_job(request):
    company_instance = Company.objects.get(id=request.session['company_instance_id'])
    add_job_form = CompanyJobForm(request.POST or None)
    if request.method == "POST":
        if add_job_form.is_valid():
            job_instance = add_job_form.save(commit=False)
            job_instance.save()
            job_prog_rel = ProgrammeJobRelation(job=job_instance)
            job_prog_rel.save()
            job_instance = get_object_or_404(Job, id=job_instance.id)
            jobid = job_instance.id
            return redirect('company_add_progs', jobid=jobid)
        else:
            return render(request, 'jobportal/Company/postjob.html', dict(add_job_form=add_job_form))
    else:
        return render(request, 'jobportal/Company/postjob.html', dict(add_job_form=add_job_form))


def add_progs(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    formset = JobProgFormSet(request.POST or None, instance=job_instance)
    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect('companyjob', jobid=job_instance.id)
        else:
            args = dict(formset=formset, job_instance=job_instance)
            return render(request, 'jobportal/Company/add_job_progs.html', args)
    else:
        args = dict(formset=formset, job_instance=job_instance)
        return render(request, 'jobportal/Company/add_job_progs.html', args)


# Candidates for a job; both alumns and students
@login_required(login_url=COMPANY_LOGIN_URL)
def company_candidates(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    # stud_list = [e.stud for e in StudentJobRelation.objects.filter(job=job_instance)]
    rel_list = StudentJobRelation.objects.filter(job=job_instance)
    hide_jobaction = True if job_instance.application_deadline > datetime.now().date() else False
    args = dict(jobid=job_instance.id, rel_list=rel_list, hide_jobaction=hide_jobaction)
    return render(request, 'jobportal/Company/candidates.html', args)


# Student Job Relation Views
@login_required(login_url=COMPANY_LOGIN_URL)
def job_stud_relation(request, jobid, studid):
    stud_instance = get_object_or_404(Student, id=studid)
    job_instance = get_object_or_404(Job, id=jobid)
    relation_instance = get_object_or_404(StudentJobRelation, stud=stud_instance, job=job_instance)
    args = dict(stud_instance=stud_instance, job_instance=job_instance, relation_instance=relation_instance)
    return render(request, 'jobportal/Company/jobactions.html', args)


# Student Shortlist
@login_required(login_url=COMPANY_LOGIN_URL)
def job_shortlist(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.shortlist_init = True
    relation_instance.save()
    return redirect("jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


# Student Unshortlist
@login_required(login_url=COMPANY_LOGIN_URL)
def job_unshortlist(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.shortlist_init = False
    relation_instance.save()
    return redirect("jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


# Student Place
@login_required(login_url=COMPANY_LOGIN_URL)
def job_place(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.placed_init = True
    relation_instance.save()
    return redirect("jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


# Student Unplace
@login_required(login_url=COMPANY_LOGIN_URL)
def job_unplace(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.placed_init = False
    relation_instance.save()
    return redirect("jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


@login_required(login_url=COMPANY_LOGIN_URL)
def job_drop(request, jobid):
    # TODO: Check no shortlist bug
    job_instance = get_object_or_404(Job, id=jobid)
    stud_rels = list(StudentJobRelation.objects.get(job=job_instance, dropped=False))
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


# Alum Job Relation Views
@login_required(login_url=COMPANY_LOGIN_URL)
def job_alum_relation(request, jobid, alumid):
    alum_instance = get_object_or_404(Alumni, id=alumid)
    job_instance = get_object_or_404(Job, id=jobid)
    relation_instance = get_object_or_404(AlumJobRelation, alum=alum_instance, job=job_instance)
    args = {'alum_instance': alum_instance,
            'job_instance': job_instance,
            'relation_instance': relation_instance
            }
    return render(request, 'jobportal/Company/jobactions.html', args)


# Alum Shortlist
@login_required(login_url=COMPANY_LOGIN_URL)
def job_shortlist2(request, relationid):
    relation_instance = get_object_or_404(AlumJobRelation, id=relationid)
    relation_instance.shortlist_status = True
    relation_instance.save()
    return redirect("jobaction2", jobid=relation_instance.job.id, alumid=relation_instance.alum.id)


# Alum Unshortlist
@login_required(login_url=COMPANY_LOGIN_URL)
def job_unshortlist2(request, relationid):
    relation_instance = get_object_or_404(AlumJobRelation, id=relationid)
    relation_instance.shortlist_status = False
    relation_instance.save()
    return redirect("jobaction2", jobid=relation_instance.job.id, alumid=relation_instance.alum.id)


# Alum Place
@login_required(login_url=COMPANY_LOGIN_URL)
def job_place2(request, relationid):
    relation_instance = get_object_or_404(AlumJobRelation, id=relationid)
    relation_instance.placed_init=True
    relation_instance.save()
    return redirect("jobaction2", jobid=relation_instance.job.id, alumid=relation_instance.alum.id)


# Alum Unplace
@login_required(login_url=COMPANY_LOGIN_URL)
def job_unplace2(request, relationid):
    relation_instance = get_object_or_404(AlumJobRelation, id=relationid)
    relation_instance.placed_init = False
    relation_instance.save()
    return redirect("jobaction2", jobid=relation_instance.job.id, alumid=relation_instance.alum.id)


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

    response = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return response


# Events and status
@login_required(login_url=COMPANY_LOGIN_URL)
def company_eventsandstatus(request):
    company_instance = get_object_or_404(Company, id=request.session['company_instance_id'])
    args = {'event_list': Event.objects.filter(company_owner=company_instance)}
    return render(request, 'jobportal/Company/eventsandstatus.html', args)


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
        return get_object_or_404(Company, id=self.request.session['company_instance_id'])


class ProfileUpdate(UpdateView):
    form_class = CompanyProfileEdit
    template_name = 'jobportal/Company/profile_update.html'
    success_url = reverse_lazy('company-profile-detail')

    def get_object(self, queryset=None):
        return get_object_or_404(Company, id=self.request.session['company_instance_id'])


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
        return Job.objects.filter(company_owner__id=self.request.session['company_instance_id'], is_deleted=False)


class JobCreate(CreateView):
    form_class = CompanyJobForm
    template_name = 'jobportal/Company/job_create.html'

    def form_valid(self, form):
        job = form.save(commit=False)
        job.posted_by_alumnus = False
        job.posted_by_company = True
        job.company_owner = Company.objects.get(id=self.request.session['company_instance_id'])
        return super(JobCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('company-job-detail', args=(self.object.id,))


class JobDetail(DetailView):
    model = Job
    template_name = 'jobportal/Company/job_detail.html'
    context_object_name = 'job'

    def get_object(self, queryset=None):
        job = Job.objects.get(id=self.kwargs['pk'])
        company = Company.objects.get(id=self.request.session['company_instance_id'])
        if job.company_owner == company:
            return job
        else:
            return Http404('You are not permitted to vie this page')


class JobUpdate(UpdateView):
    form_class = CompanyJobForm
    template_name = 'jobportal/Company/job_update.html'
    context_object_name = 'job'

    def form_valid(self, form):
        job = form.save(commit=False)
        job.last_updated = datetime.now()
        return super(JobUpdate, self).form_valid(form)

    def get_object(self, queryset=None):
        job = get_object_or_404(Job, id=self.kwargs['pk'])
        company = Company.objects.get(id=self.request.session['company_instance_id'])
        if job.company_owner == company:
            return job
        else:
            return Http404('You are not permitted to view this page')

    def get_success_url(self):
        return reverse_lazy('company-job-detail', args=(self.object.id,))


class JobDelete(View):

    def get(self, request, pk):
        job = Job.objects.get(id=pk)
        if job.company_owner.id == request.session['company_instance_id']:
            job.is_deleted = True
            job.save()
            return redirect('company-job-list')
        else:
            return Http404('You are not permitted to vie this page')


class JobRelList(ListView):
    template_name = 'jobportal/Company/jobrel_list.html'
    context_object_name = 'rel_list'

    def get_queryset(self):
        return StudentJobRelation.objects.filter(job__id=self.kwargs['pk'])


class JobRelDetail(DetailView):
    model = StudentJobRelation
    template_name = 'jobportal/Company/jobrel-detail.html'


class JobRelShortlist(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('company-jobrel-detail', pk=kwargs['pk'])

    def get(self, request, *args, **kwargs):
        jobrel = StudentJobRelation.objects.get(id=kwargs['pk'])
        jobrel.shortlist_init = False
        jobrel.save()
        return super(JobRelShortlist, self).get(*args, **kwargs)
