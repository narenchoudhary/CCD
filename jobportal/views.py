from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (View, ListView, TemplateView, DetailView, CreateView,
                                  UpdateView, RedirectView)

from .models import (UserProfile, Admin, Student, Company, Alumni, StudentJobRelation,
                     Event, Job, ProgrammeJobRelation, Avatar, Signature, CV)
from .forms import LoginForm, EditStudProfileForm, SelectCVForm, AvatarForm, SignatureForm

STUD_LOGIN_URL = reverse_lazy('login')
ALUM_LOGIN_URL = reverse_lazy('login')
COMPANY_LOGIN_URL = reverse_lazy('login')


def get_questions(studid):
    stud_instance = get_object_or_404(Student, id=studid)
    questions = []
    if bool(stud_instance.cv1):
        questions.append("cv1")
    if bool(stud_instance.cv2):
        questions.append("cv2")
    return questions


def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
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
        args = dict(form=form)
        return render(request, 'jobportal/login.html', args)


@login_required(login_url=reverse_lazy('login'))
def stud_applyjob(request, jobid):
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    job_instance = get_object_or_404(Job, id=jobid)
    form = SelectCVForm(request.POST or None, extra=get_questions(student_instance.id))
    if request.method == "POST":
        if form.is_valid():
            relation_instance = StudentJobRelation(
                stud=student_instance,
                job=job_instance
            )
            relation_instance.save()
            for (question, answer) in form.extra_answers():
                setattr(relation_instance, question, answer)
            relation_instance.save()
            return redirect('jobdetails', jobid=jobid)
        else:
            args = dict(form=form, jobid=jobid)
            return render(request, 'jobportal/Student/apply.html', args)
    else:
        args = dict(form=form, jobid=jobid)
        return render(request, 'jobportal/Student/apply.html', args)


@login_required(login_url=reverse_lazy('login'))
def stud_deapplyjob(request, jobid):
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    job_instance = Job.objects.get(id=jobid)
    relation_instance = get_object_or_404(StudentJobRelation, stud=student_instance, job=job_instance)
    relation_instance.delete()
    return redirect('jobdetails', jobid=jobid)


@login_required(login_url=reverse_lazy('login'))
def stud_jobsappliedfor(request):
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    job_list = [e.job for e in StudentJobRelation.objects.filter(stud=student_instance)]
    args = {'job_list': job_list}
    return render(request, 'jobportal/Student/appliedfor.html', args)


@login_required(login_url=reverse_lazy('login'))
def stud_jobdetails(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    deadline_gone = True if job_instance.application_deadline < datetime.now().date() else False
    nocv = True if not bool(student_instance.cv1) and not bool(student_instance.cv2) else False
    args = {'job_instance': job_instance, 'deadline_gone': deadline_gone, 'nocv': nocv}
    try:
        relation_instance = StudentJobRelation.objects.get(stud=student_instance, job=job_instance)
    except StudentJobRelation.DoesNotExist:
        relation_instance = None
    args['relation_instance'] = relation_instance
    return render(request, "jobportal/Student/jobdetail.html", args)


class LogoutView(View):

    def get(self, request):
        if request.user and request.user.is_authenticated():
            auth.logout(request)
        return redirect('index')


class HomeView(TemplateView):

    template_name = 'jobportal/Student/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['stud'] = Student.objects.get(user=self.request.user)
        return context


class ProfileDetail(DetailView):
    model = Student
    template_name = 'jobportal/Student/profile_detail.html'


class ProfileUpdate(UpdateView):
    form_class = EditStudProfileForm
    template_name = 'jobportal/Student/profile_update.html'
    success_url = reverse_lazy('stud-home')

    def get_object(self, queryset=None):
        return get_object_or_404(Student, id=self.request.session['student_instance_id'])


class JobList(ListView):
    queryset = Job.objects.all()
    template_name = 'jobportal/Student/job_list.html'
    context_object_name = 'job_list'


class JobDetail(DetailView):
    model = Job
    template_name = 'jobportal/Student/job_detail.html'


class JobRelList(ListView):
    template_name = 'jobportal/Student/jobrel_list.html'

    def get_queryset(self):
        stud_object = Student.objects.get(user=self.request.user)
        return StudentJobRelation.objects.filter(stud=stud_object)


class JobRelDetail(DetailView):
    model = ProgrammeJobRelation
    template_name = 'jobportal/Student/jobrel_detail.html'


class EventList(ListView):
    queryset = Event.objects.all()
    template_name = 'jobportal/Student/event_list.html'
    context_object_name = 'event_list'


class EventDetail(DetailView):
    model = Event
    template_name = 'jobportal/Student/event_detail.html'


class AvatarDetail(DetailView):
    model = Avatar
    template_name = 'jobportal/Student/avatar_detail.html'
    context_object_name = 'avatar'

    def get_object(self, queryset=None):
        try:
            avatar = Avatar.objects.get(stud__id=self.request.session['student_instance_id'])
        except Avatar.DoesNotExist:
            avatar = None
        return avatar


class AvatarUpdate(UpdateView):
    form_class = AvatarForm
    template_name = 'jobportal/Student/avatar_update.html'
    success_url = reverse_lazy('stud-avatar-detail')

    def get_object(self, queryset=None):
        try:
            avatar = Avatar.objects.get(stud__id=self.request.session['student_instance_id'])
        except Avatar.DoesNotExist:
            avatar = None
        return avatar


class AvatarCreate(CreateView):
    model = Avatar
    fields = ['avatar']
    template_name = 'jobportal/Student/avatar_create.html'
    success_url = reverse_lazy('stud-avatar-detail')

    def form_valid(self, form):
        avatar = form.save(commit=False)
        avatar.stud = Student.objects.get(id=self.request.session['student_instance_id'])
        return super(AvatarCreate, self).form_valid(form)


class SignatureDetail(DetailView):
    model = Signature
    template_name = 'jobportal/Student/signature_detail.html'
    context_object_name = 'signature'

    def get_object(self, queryset=None):
        try:
            signature = Signature.objects.get(stud__id=self.request.session['student_instance_id'])
        except Signature.DoesNotExist:
            signature = None
        return signature


class SignatureCreate(CreateView):
    model = Signature
    fields = ['signature']
    template_name = 'jobportal/Student/signature_create.html'
    success_url = reverse_lazy('stud-sign-detail')

    def form_valid(self, form):
        signature = form.save(commit=False)
        signature.stud = Student.objects.get(id=self.request.session['student_instance_id'])
        return super(SignatureCreate, self).form_valid(form)


class SignatureUpdate(UpdateView):
    form_class = SignatureForm
    template_name = 'jobportal/Student/signature_create.html'
    success_url = reverse_lazy('stud-sign-detail')

    def get_object(self, queryset=None):
        try:
            signature = Signature.objects.get(stud__id=self.request.session['student_instance_id'])
        except Avatar.DoesNotExist:
            signature = None
        return signature


class CVDetail(DetailView):
    model = CV
    template_name = 'jobportal/Student/cv_detail.html'
    context_object_name = 'cv'

    def get_object(self, queryset=None):
        try:
            cv = CV.objects.get(stud__id=self.request.session['student_instance_id'])
        except CV.DoesNotExist:
            cv = None
        return cv


class CVCreate(CreateView):
    model = CV
    fields = ['cv1', 'cv2']
    template_name = 'jobportal/Student/cv_create.html'
    success_url = reverse_lazy('stud-cv-detail')

    def form_valid(self, form):
        cv = form.save(commit=False)
        cv.stud = Student.objects.get(id=self.request.session['student_instance_id'])
        return super(CVCreate, self).form_valid(form)


class CVUpdate(UpdateView):
    model = CV
    fields = ['cv1', 'cv2']
    template_name = 'jobportal/Student/cv_update.html'
    success_url = reverse_lazy('stud-cv-detail')

    def get_object(self, queryset=None):
        try:
            cv = CV.objects.get(stud__id=self.request.session['student_instance_id'])
        except CV.DoesNotExist:
            cv = None
        return cv
