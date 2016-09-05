import zipfile
import os
import StringIO

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
from django.views.generic import (View, TemplateView, RedirectView, CreateView,
                                  UpdateView, ListView, DetailView)

from .models import (UserProfile, Job, Company, StudentJobRelation,
                     ProgrammeJobRelation, Event, Programme, CV)
from .forms import (CompanyProfileEdit, CompanyJobForm, CompanySignup,
                    CompanyJobRelForm, EventForm)

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
        form = CompanySignup()
        args = dict(form=form)
        return render(request, self.template, args)

    def post(self, request):
        form = CompanySignup(request.POST)
        if form.is_valid():
            username = form.cleaned_data.pop('username')
            password1 = form.cleaned_data.pop('password1')
            user = UserProfile(username=username,
                               password=make_password(password1),
                               user_type='company',
                               is_active=False)
            user.save()
            company = form.save(commit=False)
            company.user = user
            company.save()
            return render(request, 'jobportal/Company/signupconfirm.html',
                          dict(email=company.head_hr_email))
        else:
            args = dict(form=form)
            return render(request, self.template, args)


class HomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'jobportal/Company/home.html'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(user=self.request.user)
        return context


class ProfileDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Company
    template_name = 'jobportal/Company/profile_detail.html'
    context_object_name = 'company'

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_object(self, queryset=None):
        return get_object_or_404(Company,
                                 id=self.request.session['company_instance_id'])


class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    form_class = CompanyProfileEdit
    template_name = 'jobportal/Company/profile_update.html'
    success_url = reverse_lazy('company-profile-detail')

    def test_func(self):
        return self.request.user.user_type == 'company'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Company, id=self.request.session['company_instance_id'])


class PasswordChangeView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    raise_exception = True
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

    def get_object(self, queryset=None):
        return self.job

    def get_context_data(self, **kwargs):
        context = super(JobDetail, self).get_context_data(**kwargs)
        context['rel_list'] = ProgrammeJobRelation.objects.filter(
            job=self.object)
        date_today = timezone.now().date()
        context['deadline_over'] = self.job.application_deadline <= date_today
        return context


class JobUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
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
    raise_exception = True
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
        deadline_over = deadline < timezone.now().date()
        if not deadline_over:
            return False
        return True

    def get_queryset(self):
        return StudentJobRelation.objects.filter(job__id=self.kwargs[
            'pk']).order_by('placed_init', 'placed_approved', 'shortlist_init')

    def get_context_data(self, **kwargs):
        context = super(JobRelList, self).get_context_data(**kwargs)
        context['jobid'] = self.job.id
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


class EventUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    raise_exception = True
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
        deadline = job.application_deadline < timezone.now().date()
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
    login_url = reverse_lazy('login')
    template_name = 'jobportal/Company/jobprog_create.html'
    job = None

    def test_func(self):
        is_company = self.request.user.user_type == 'company'
        if not is_company:
            return False
        self.job = get_object_or_404(Job, id=self.kwargs['jobpk'])
        session_id = self.request.session['company_instance_id']
        is_owner = self.job.company_owner.id == session_id
        if not is_owner:
            return False
        deadline_ok = self.job.application_deadline > timezone.now().date()
        if not deadline_ok:
            return False
        return True

    def get(self, request, jobpk):
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
        btech_bdes_list_ids = request.POST.getlist('selected_btech_bdes_ids')
        mtech_mdes_list_ids = request.POST.getlist('selected_mtech_mdes_ids')
        phd_list_ids = request.POST.getlist('selected_phd_ids')
        ma_list_ids = request.POST.getlist('selected_ma_ids')
        msc_list_ids = request.POST.getlist('selected_msc_ids')

        programme_list = Programme.objects.filter(
            Q(id__in=minor_list_ids) |
            Q(id__in=btech_bdes_list_ids) |
            Q(id__in=phd_list_ids) |
            Q(id__in=ma_list_ids) |
            Q(id__in=mtech_mdes_list_ids) |
            Q(id__in=msc_list_ids)
        )

        for programme in programme_list:

            ProgrammeJobRelation.objects.get_or_create(
                job=job,
                year=programme.year,
                dept=programme.dept,
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
        download_name = job.company_owner.user.username + '_' + job.designation
        response['Content-Disposition'] = 'attachment; filename=%s' % \
                                          smart_str(download_name)
        return response
