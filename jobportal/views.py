from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import (View, ListView, TemplateView, DetailView, CreateView, UpdateView)

from .models import (UserProfile, Admin, Student, Company, Alumni, StudentJobRelation, Event, Job,
                     ProgrammeJobRelation, MinorProgrammeJobRelation, Avatar, Signature, CV)
from .forms import LoginForm, EditStudProfileForm, SelectCVForm, CVForm

STUD_LOGIN_URL = reverse_lazy('login')
ALUM_LOGIN_URL = reverse_lazy('login')
COMPANY_LOGIN_URL = reverse_lazy('login')


def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        # https://docs.djangoproject.com/en/1.9/topics/http/sessions/#setting-test-cookies
        print request.session.test_cookie_worked()
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_active is True:
                    user_profile = UserProfile.objects.get(username=username)
                    if user_profile.user_type == 'student':
                        auth.login(request, user)
                        student_instance = Student.objects.get(user=user_profile)
                        request.session['student_instance_id'] = student_instance.id
                        request.session['login_type'] = 'student'
                        return redirect('stud-home')

                    elif user_profile.user_type == 'company':
                        auth.login(request, user)
                        company_instance = Company.objects.get(user=user_profile)
                        request.session['company_instance_id'] = company_instance.id
                        request.session['login_type'] = 'company'
                        return redirect('company-home')

                    elif user_profile.user_type == 'alumni':
                        auth.login(request, user)
                        alum_instance = Alumni.objects.get(user=user_profile)
                        request.session['alum_instance_id'] = alum_instance.id
                        request.session['login_type'] = 'alumni'
                        return redirect('alum_home')

                    elif user_profile.user_type == 'admin':
                        auth.login(request, user)
                        admin_instance = Admin.objects.get(user=user_profile)
                        request.session['admin_instance_id'] = admin_instance.id
                        request.session['login_type'] = 'admin'
                        return redirect('admin-home')

                    else:
                        # this case should never happen unless new users are added
                        args = dict(form=form)
                        return render(request, 'jobportal/login.html', args)
                else:
                    args = dict(form=form)
                    return render(request, 'jobportal/login.html', args)
            else:
                args = dict(form=form)
                return render(request, 'jobportal/login.html', args)
        else:
            return HttpResponse("Please enable cookies and try again.")
    else:
        # https://docs.djangoproject.com/en/1.9/topics/http/sessions/#setting-test-cookies
        request.session.set_test_cookie()
        return render(request, 'jobportal/login.html', dict(form=form))


class LogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        if request.user and request.user.is_authenticated():
            auth.logout(request)
        return redirect('index')


class HomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    login_url = reverse_lazy('login')
    raise_exception = True
    template_name = 'jobportal/Student/home.html'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['stud'] = Student.objects.get(user=self.request.user)
        return context


class ProfileDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):

    login_url = reverse_lazy('login')
    raise_exception = True
    model = Student
    template_name = 'jobportal/Student/profile_detail.html'

    def test_func(self):
        return self.request.user.user_type == 'student'


class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    form_class = EditStudProfileForm
    template_name = 'jobportal/Student/profile_update.html'
    success_url = reverse_lazy('stud-home')

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        return get_object_or_404(Student, id=self.request.session['student_instance_id'])


class JobList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    raise_exception = True
    template_name = 'jobportal/Student/job_list.html'
    context_object_name = 'job_list'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_queryset(self):
        stud = get_object_or_404(Student, id=self.request.session['student_instance_id'])
        # Ref: http://stackoverflow.com/a/12600950/3679857
        major = ProgrammeJobRelation.objects.filter(prog=stud.prog)
        minor = MinorProgrammeJobRelation.objects.filter(prog=stud.minor_prog)
        return Job.objects.filter(
            Q(id__in=major.values('job_id')) | Q(id__in=minor.values('job_id'))
        ).filter(
            Q(cpi_shortlist=False) | Q(cpi_shortlist=True, minimum_cpi__lte=stud.cpi)
        ).filter(
            approved=True
        ).filter(
            opening_date__lte=timezone.now().date()
        ).filter(
            application_deadline__gt=timezone.now().date()
        ).filter(
            percentage_x__gte=stud.percentage_x
        ).filter(
            percentage_xii__gte=stud.percentage_xii
        )

    def get_context_data(self, **kwargs):
        context = super(JobList, self).get_context_data(**kwargs)
        context['stud'] = get_object_or_404(Student, id=self.request.session['student_instance_id'])
        return context


class JobDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Job
    template_name = 'jobportal/Student/job_detail.html'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_context_data(self, **kwargs):
        context = super(JobDetail, self).get_context_data(**kwargs)
        context['no_cv'] = self.student_cv()
        context['now'] = timezone.now()
        context['jobrel'] = self.get_jobrel_or_none(self.kwargs['pk'])
        return context

    def student_cv(self):
        cv = get_object_or_404(CV, stud__id=self.request.session['student_instance_id'])
        if cv.cv1 is None and cv.cv2 is None:
            return True
        return False

    def get_jobrel_or_none(self, jobid):
        try:
            jobrel = StudentJobRelation.objects.get(job__id=jobid,
                                                    stud__id=self.request.session['student_instance_id'])
            return jobrel
        except StudentJobRelation.DoesNotExist:
            return None


class JobRelList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    raise_exception = True
    template_name = 'jobportal/Student/jobrel_list.html'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_queryset(self):
        return StudentJobRelation.objects.filter(stud__id=self.request.session['student_instance_id'])


class JobRelDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = ProgrammeJobRelation
    template_name = 'jobportal/Student/jobrel_detail.html'

    def test_func(self):
        return self.request.user.user_type == 'student'


class JobRelCreate(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    raise_exception = True
    stud = None
    job = None
    template = 'jobportal/Student/jobrel_create.html'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get(self, request, pk):
        self.stud = get_object_or_404(Student, id=request.session['student_instance_id'])
        self.job = get_object_or_404(Job, id=pk)
        stud_check = self.check_stud_credentials()
        job_check = self.check_job_credentials()
        job_check = True
        print stud_check
        print job_check
        if stud_check and job_check:
            form = SelectCVForm(extra=self.get_questions())
            return render(request, self.template, dict(form=form, job=self.job))
        else:
            return redirect('stud-job-list')

    def post(self, request, pk):
        self.job = get_object_or_404(Job, id=pk)
        self.stud = get_object_or_404(Student, id=request.session['student_instance_id'])
        stud_check = self.check_stud_credentials()
        # job_check = self.check_job_credentials()
        job_check = True
        if stud_check and job_check:
            form = SelectCVForm(request.POST, extra=self.get_questions())
            if form.is_valid():
                jobrel = StudentJobRelation(stud=self.stud, job=self.job)
                jobrel.save()
                for (question, answer) in form.extra_answers():
                    setattr(jobrel, question, answer)
                jobrel.save()
                return redirect('stud-job-detail', pk=self.job.id)
        return redirect('stud-job-list')

    def get_questions(self):
        cv = get_object_or_404(CV, stud=self.stud)
        questions = []
        if bool(cv.cv1):
            questions.append("cv1")
        if bool(cv.cv2):
            questions.append("cv2")
        return questions

    def check_stud_credentials(self):
        try:
            cv = CV.objects.get(stud=self.stud)
        except CV.DoesNotExist:
            return False
        if bool(cv.cv1) or bool(cv.cv2):
            return True
        else:
            return False

    def check_job_credentials(self):
        time_now = timezone.now().date()
        opening_date_check = self.job.opening_date <= time_now
        deadline_check = self.job.application_deadline >= time_now
        approved_check = self.job.approved is True
        return opening_date_check and deadline_check and approved_check


class JobRelDelete(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    raise_exception = True
    stud = None
    job = None
    jobrel = None

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get(self, request, pk):
        self.stud = get_object_or_404(Student, id=request.session['student_instance_id'])
        self.job = get_object_or_404(Job, id=pk)
        self.jobrel = get_object_or_404(StudentJobRelation, stud=self.stud, job=self.job)
        job_check = self.check_job_credentials()
        print job_check
        if job_check:
            self.jobrel.delete()
            return redirect('stud-job-detail', pk=self.job.id)
        else:
            return redirect('stud-job-detail', pk=self.job.id)

    def check_job_credentials(self):
        time_now = timezone.now().date()
        opening_date_check = self.job.opening_date <= time_now
        deadline_check = self.job.application_deadline > time_now
        approved_check = self.job.approved is True
        return opening_date_check and deadline_check and approved_check


class EventList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = Event.objects.all()
    template_name = 'jobportal/Student/event_list.html'
    context_object_name = 'event_list'


class EventDetail(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Event
    template_name = 'jobportal/Student/event_detail.html'


class AvatarDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Avatar
    template_name = 'jobportal/Student/avatar_detail.html'
    context_object_name = 'avatar'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        try:
            avatar = Avatar.objects.get(stud__id=self.request.session['student_instance_id'])
        except Avatar.DoesNotExist:
            avatar = None
        return avatar


class AvatarUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Avatar
    fields = ['avatar']
    template_name = 'jobportal/Student/avatar_update.html'
    success_url = reverse_lazy('stud-avatar-detail')

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        try:
            avatar = Avatar.objects.get(stud__id=self.request.session['student_instance_id'])
        except Avatar.DoesNotExist:
            avatar = None
        return avatar


class AvatarCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Avatar
    fields = ['avatar']
    template_name = 'jobportal/Student/avatar_create.html'
    success_url = reverse_lazy('stud-avatar-detail')

    def test_func(self):
        return self.request.user.user_type == 'student'

    def form_valid(self, form):
        avatar = form.save(commit=False)
        avatar.stud = Student.objects.get(id=self.request.session['student_instance_id'])
        return super(AvatarCreate, self).form_valid(form)


class SignatureDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Signature
    template_name = 'jobportal/Student/signature_detail.html'
    context_object_name = 'signature'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        try:
            signature = Signature.objects.get(stud__id=self.request.session['student_instance_id'])
        except Signature.DoesNotExist:
            signature = None
        return signature


class SignatureCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Signature
    fields = ['signature']
    template_name = 'jobportal/Student/signature_create.html'
    success_url = reverse_lazy('stud-sign-detail')

    def test_func(self):
        return self.request.user.user_type == 'student'

    def form_valid(self, form):
        signature = form.save(commit=False)
        signature.stud = Student.objects.get(id=self.request.session['student_instance_id'])
        return super(SignatureCreate, self).form_valid(form)


class SignatureUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Signature
    fields = ['signature']
    template_name = 'jobportal/Student/signature_update.html'
    success_url = reverse_lazy('stud-sign-detail')

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        try:
            signature = Signature.objects.get(stud__id=self.request.session['student_instance_id'])
        except Avatar.DoesNotExist:
            signature = None
        return signature


class CVDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = CV
    template_name = 'jobportal/Student/cv_detail.html'
    context_object_name = 'cv'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        try:
            cv = CV.objects.get(stud__id=self.request.session['student_instance_id'])
        except CV.DoesNotExist:
            cv = None
        return cv


class CVCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    form_class = CVForm
    template_name = 'jobportal/Student/cv_create.html'
    success_url = reverse_lazy('stud-cv-detail')

    def test_func(self):
        return self.request.user.user_type == 'student'

    def form_valid(self, form):
        cv = form.save(commit=False)
        cv.stud = Student.objects.get(id=self.request.session['student_instance_id'])
        return super(CVCreate, self).form_valid(form)


class CVUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = CV
    fields = ['cv1', 'cv2']
    template_name = 'jobportal/Student/cv_update.html'
    success_url = reverse_lazy('stud-cv-detail')

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        try:
            cv = CV.objects.get(stud__id=self.request.session['student_instance_id'])
        except CV.DoesNotExist:
            cv = None
        return cv
