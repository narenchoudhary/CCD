import poplib

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.forms import FileInput
from django.forms.models import modelform_factory
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.encoding import smart_str
from django.views.generic import (View, ListView, TemplateView, DetailView,
                                  CreateView, UpdateView)

from .models import (UserProfile, Admin, Student, Company, Programme,
                     StudentJobRelation, Event, Job, ProgrammeJobRelation,
                     Avatar, Signature, CV, SiteManagement)
from .forms import LoginForm, EditStudProfileForm, SelectCVForm, CVForm

STUD_LOGIN_URL = reverse_lazy('login')
ALUM_LOGIN_URL = reverse_lazy('login')
COMPANY_LOGIN_URL = reverse_lazy('login')


def handler400(request):
    return render(request, '400.html')


def handler403(request):
    return render(request, '403.html')


def handler404(request):
    return render(request, '404.html')


def handler500(request):
    return render(request, '500.html')


def handler503(request):
    return render(request, '503.html')


def check_webmail_auth_at_server():
    return


class Login(View):
    template_name = 'jobportal/login.html'
    server_dict = {
        'dikrong': '202.141.80.13',
        # 'teesta': '202.141.80.12',
        'tamdil': '202.141.80.11',
        # 'naambor': '202.141.80.9',
        'disbang': '202.141.80.10'
    }
    server_port = 995

    def _auth_one_server(self, username, password, server):
        """
        :param username: username
        :param password: password
        :param server: server name, not ip
        :return: login status
        """
        server_ip = self.server_dict.get(str(server).lower())
        print("server and ip : %s and %s " % (server, server_ip))
        try:
            print("server poplib start")
            print(server_ip)
            print(type(server_ip))
            serv = poplib.POP3_SSL(server_ip, self.server_port)
            print('serv_created')
            serv.user(username)
            print("username complete")
            p_str = serv.pass_(password)
            print("password complete")
            if 'OK' in p_str:
                serv.quit()
                print("all OK and True")
                return True
        except poplib.error_proto:
            serv.quit()
            print("poplib.error_proto: -ERR Authentication failed.")
            return False
        except:
            print("exception and False")
            return False
        print("no exception and False")
        return False

    def _auth_all_servers(self, username, password):
        """
        :param username: username
        :param password: password
        :return: matching_server, login_status

        login_status == False implies wrong_password.
        """
        for server in self.server_dict.items():
            print("Auth all servers with %s" % server[0])
            status = self._auth_one_server(username, password, server[0])
            print("%s returned %s" % (server[0], str(status)))
            if status:
                print("Lgin success")
                return server[0], True
            print("Iteration for another server")
        return None, False

    def get(self, request):
        form = LoginForm(None)
        if request.user.is_authenticated():
            userprofile = UserProfile.objects.get(
                username=request.user.username)
            user_type = userprofile.user_type
            if user_type == 'admin':
                if Admin.objects.filter(user=userprofile).exists():
                    return redirect('admin-home')
            elif user_type == 'company':
                if Company.objects.filter(user=userprofile).exists():
                    return redirect('company-home')
            elif user_type == 'student':
                if Student.objects.filter(user=userprofile).exists():
                    return redirect('stud-home')
            elif user_type == 'verifier':
                return redirect('verifier-home')
            else:
                auth.logout(request)
        # https://docs.djangoproject.com/en/1.9/topics/http/sessions/#setting-test-cookies
        request.session.set_test_cookie()
        return render(request, self.template_name, dict(form=form))

    def post(self, request):
        form = LoginForm(request.POST)
        # https://docs.djangoproject.com/en/1.9/topics/http/sessions/#setting-test-cookies
        if request.session.test_cookie_worked():
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                remember_me = form.cleaned_data['remember_me']
                if not remember_me:
                    request.session.set_expiry(0)
                try:
                    user_profile = UserProfile.objects.get(username=username)
                except UserProfile.DoesNotExist:
                    user_profile = None
                if user_profile is not None:
                    user_type = user_profile.user_type
                    if user_type == 'admin' and \
                            Admin.objects.filter(user=user_profile).exists():
                        if user_profile.is_active:
                            user = auth.authenticate(username=username,
                                                     password=password)
                            if user is not None:
                                auth.login(request, user)
                                admin = Admin.objects.get(
                                    user=user_profile)
                                request.session['admin_instance_id'] = admin.id
                                return redirect('admin-home')
                            else:
                                error = 'Incorrect password.'
                                args = dict(form=form, error=error)
                                return render(request, self.template_name,
                                              args)

                        else:
                            error = 'User not active yet.'
                            args = dict(form=form, error=error)
                            return render(request, self.template_name, args)
                    elif user_type == 'verifier':
                        if user_profile.is_active:
                            user = auth.authenticate(username=username,
                                                     password=password)
                            if user is not None:
                                auth.login(request, user)
                                request.session['verifier_instance_id'] = \
                                    user_profile.id
                                return redirect('verifier-home')
                            else:
                                error = 'Incorrect password.'
                                args = dict(form=form, error=error)
                                return render(request, self.template_name,
                                              args)
                        else:
                            error = 'User not active yet.'
                            args = dict(form=form, error=error)
                            return render(request, self.template_name, args)
                    elif user_type == 'company':
                        if user_profile.is_active:
                            user = auth.authenticate(username=username,
                                                     password=password)
                            if user is not None:
                                auth.login(request, user)
                                company = Company.objects.get(
                                    user=user_profile)
                                request.session['company_instance_id'] = company.id
                                return redirect('company-home')
                            else:
                                error = 'Incorrect password.'
                                args = dict(form=form, error=error)
                                return render(request, self.template_name,
                                              args)
                        else:
                            error = 'Your signup request has not been ' \
                                    'approved yet. Please visit again after ' \
                                    'some time.'
                            args = dict(form=form, error=error)
                            return render(request, self.template_name, args)
                    elif user_type == 'student':
                        # fee paid
                        if user_profile.is_active:
                            # check if server is saved
                            if bool(user_profile.login_server):
                                print("Student login_server found.")
                                status = self._auth_one_server(
                                    username=username, password=password,
                                    server=user_profile.login_server)
                                # if saved server worked
                                if status:
                                    print("Login Successful for login_server")
                                    # authenticate
                                    # TODO: Write auth backend
                                    # http://stackoverflow.com/a/2788053/3679857
                                    # password=username is a just hack
                                    # This is not good design, but it saved me
                                    # from writing custom auth backend
                                    user = auth.authenticate(username=username,
                                                             password=username)
                                    if user is not None:
                                        auth.login(request, user)
                                        stud = Student.objects.get(
                                            user=user_profile
                                        )
                                        request.session[
                                            'student_instance_id'] = stud.id
                                        return redirect('stud-home')
                                # if saved server did not work
                                else:
                                    print("Login Failed for login_server")
                                    # try all the servers
                                    print("Login Successful")
                                    server, status = self._auth_all_servers(
                                        username=username, password=password
                                    )
                                    # if match found
                                    if status:
                                        # save server for future logins
                                        user_profile.server = True
                                        user_profile.save()
                                        # authenticate and authorize
                                        user = auth.authenticate(
                                            username=username,
                                            password=username)
                                        auth.login(request, user)
                                        stud = Student.objects.get(
                                            user=user_profile
                                        )
                                        request.session[
                                            'student_instance_id'] = stud.id
                                        return redirect('stud-home')
                                    else:
                                        error = 'Wrong password'
                                        args = dict(form=form, error=error)
                                        return render(
                                            request, self.template_name, args
                                        )
                            # if server is not saved
                            else:
                                server, status = self._auth_all_servers(
                                    username=username, password=password
                                )
                                # if match found
                                if status:
                                    # saved server for future requests
                                    user_profile.login_server = server
                                    user_profile.save()
                                    # authenticate and authorize
                                    user = auth.authenticate(
                                        username=username, password=password)
                                    auth.login(request, user)
                                    stud = Student.objects.get(
                                        user=user_profile
                                    )
                                    request.session[
                                        'student_instance_id'] = stud.id
                                    return redirect('student-home')
                                else:
                                    error = 'Wrong password'
                                    args = dict(form=form, error=error)
                                    return render(request, self.template_name,
                                                  args)

                        else:
                            error = 'Fee not paid'
                            args = dict(form=form, error=error)
                            return render(request, self.template_name, args)
                    elif user_type == 'alumni':
                        pass
                    else:
                        error = 'User has not been activated yet.'
                        args = dict(form=form, error=error)
                        return render(request, self.template_name, args)
                else:
                    error = 'Invalid username'
                    args = dict(form=form, error=error)
                    return render(request, self.template_name, args)
            else:
                return render(request, self.template_name, dict(form=form))

        else:
            error = 'Please enable cookies and try again.'
            args = dict(form=form, error=error)
            return render(request, self.template_name, args)


class Logout(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user and self.request.user.is_authenticated()

    def get(self, request):
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
    context_object_name = 'student'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Student, id=self.request.session['student_instance_id'])

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['site_management'] = SiteManagement.objects.all()[0]
        return context


class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    form_class = EditStudProfileForm
    template_name = 'jobportal/Student/profile_update.html'
    success_url = reverse_lazy('stud-profile-detail')

    def test_func(self):
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        site_model = SiteManagement.objects.all()[0]
        now = timezone.now()
        date_passed = site_model.job_student_profile_update_deadline < now
        if date_passed:
            return False
        return True

    def get_object(self, queryset=None):
        return get_object_or_404(
            Student,
            id=self.request.session['student_instance_id'])


class JobList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    raise_exception = True
    template_name = 'jobportal/Student/job_list.html'
    context_object_name = 'job_list'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_queryset(self):
        stud = get_object_or_404(
            Student, id=self.request.session['student_instance_id'])
        # Ref: http://stackoverflow.com/a/12600950/3679857
        try:
            prog = Programme.objects.get(
                year=stud.year, dept=stud.dept, name=stud.prog,
                discipline=stud.discipline, minor_status=False,
                open_for_placement=True)
        except Programme.DoesNotExist:
            prog = None
        try:
            minor_prog = Programme.objects.get(
                year=stud.minor_year, dept=stud.minor_dept,
                name=stud.minor_prog, discipline=stud.minor_discipline,
                minor_status=True, open_for_placement=True)
        except Programme.DoesNotExist:
            minor_prog = None

        major = ProgrammeJobRelation.objects.filter(prog=prog)
        minor = ProgrammeJobRelation.objects.filter(prog=minor_prog)

        # evil
        if stud.cpi < 5:
            return None

        # fix for filtering is CGPA is filled
        # multiply CGPA by 10 before filtering
        stud_percentage_x = stud.percentage_x
        if stud_percentage_x <= 10:
            stud_percentage_x *= 10
        stud_percentage_xii = stud.percentage_xii
        if stud_percentage_xii <= 10:
            stud_percentage_xii *= 10

        # return job queryset obtained by filtering against required checks
        return Job.objects.filter(
            Q(id__in=major.values('job_id')) | Q(id__in=minor.values('job_id'))
        ).filter(
            Q(cpi_shortlist=False) | Q(cpi_shortlist=True,
                                       minimum_cpi__lte=stud.cpi)
        ).filter(
            Q(backlog_filter=False) |
            Q(backlog_filter=True,
              num_backlogs_allowed__gte=stud.active_backlogs)
        ).filter(
            approved=True
        ).filter(
            opening_datetime__lte=timezone.now()
        ).filter(
            application_deadline__gte=timezone.now()
        ).filter(
            percentage_x__lte=stud_percentage_x
        ).filter(
            percentage_xii__lte=stud_percentage_xii
        )

    def get_context_data(self, **kwargs):
        context = super(JobList, self).get_context_data(**kwargs)
        context['stud'] = get_object_or_404(
            Student, id=self.request.session['student_instance_id'])
        return context


# TODO: Test this view
class JobDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Job
    template_name = 'jobportal/Student/job_detail.html'
    stud = None
    jobid = None
    job = None
    prog = None
    minor_prog = None

    def test_func(self):
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        self.stud = get_object_or_404(
            Student, id=self.request.session['student_instance_id'])
        self.jobid = self.kwargs['pk']
        self.job = get_object_or_404(Job, id=self.jobid)
        # TODO: Check eligibility
        stud_eligibility = self.check_student_eligibility()
        if not stud_eligibility:
            return False
        return True

    def get_context_data(self, **kwargs):
        context = super(JobDetail, self).get_context_data(**kwargs)
        context['no_cv'] = self.no_cv()
        now = timezone.now()
        context['deadline_passed'] = self.job.application_deadline < now
        context['jobrel'] = self.get_jobrel_or_none()
        return context

    def no_cv(self):
        """
        Return True when student has not uploaded any CV
        :return: status of CV
        """
        try:
            cv = CV.objects.get(
                stud__id=self.request.session['student_instance_id'])
        except CV.DoesNotExist:
            return True
        if cv.cv1 is None and cv.cv2 is None:
            return True
        return False

    def get_jobrel_or_none(self):
        try:
            jobrel = StudentJobRelation.objects.get(
                job__id=self.jobid,
                stud__id=self.stud.id)
            return jobrel
        except StudentJobRelation.DoesNotExist:
            return None

    def check_student_eligibility(self):
        # Check Programme eligibility
        try:
            self.prog = Programme.objects.get(
                year=self.stud.year, dept=self.stud.dept,
                name=self.stud.prog, discipline=self.stud.discipline,
                minor_status=False, open_for_placement=True)
        except Programme.DoesNotExist:
            pass
        try:
            self.minor_prog = Programme.objects.get(
                year=self.stud.minor_year, dept=self.stud.minor_dept,
                name=self.stud.minor_prog, open_for_placement=True,
                discipline=self.stud.minor_discipline, minor_status=True
                )
        except Programme.DoesNotExist:
            pass
        progjobrel = ProgrammeJobRelation.objects.filter(
            Q(job=self.job, prog=self.prog) |
            Q(job=self.job, prog=self.minor_prog)
        )
        if not progjobrel:
            return False
        # Check CPI eligibility
        if self.job.cpi_shortlist and self.job.minimum_cpi > self.stud.cpi:
            return False
        # Check BackLog eligibility
        if self.job.backlog_filter and self.job.num_backlogs_allowed < \
                self.stud.active_backlogs:
            return False
        return True


class JobRelList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    raise_exception = True
    template_name = 'jobportal/Student/jobrel_list.html'
    context_object_name = 'jobrel_list'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_queryset(self):
        return StudentJobRelation.objects.filter(
            stud__id=self.request.session['student_instance_id'])


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
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        self.stud = get_object_or_404(
            Student, id=self.request.session['student_instance_id'])
        self.job = get_object_or_404(Job, id=self.kwargs['pk'])
        stud_cv_check = self.check_stud_credentials()
        stud_check = self.check_stud_credentials()
        job_check = self.check_job_credentials()
        if not stud_cv_check or not stud_check or not job_check:
            return False
        return True

    def get(self, request, pk):
        form = SelectCVForm(extra=self.get_questions())
        return render(request, self.template, dict(form=form, job=self.job))

    def post(self, request, pk):
        form = SelectCVForm(request.POST, extra=self.get_questions())
        if form.is_valid():
            jobrel = StudentJobRelation(stud=self.stud, job=self.job)
            jobrel.save()
            for (question, answer) in form.extra_answers():
                setattr(jobrel, str(question).lower(), answer)
            jobrel.save()
            return redirect('stud-job-detail', pk=self.job.id)
        else:
            return render(request, self.template,
                          dict(form=form, job=self.job))

    def get_questions(self):
        cv = get_object_or_404(CV, stud=self.stud)
        questions = []
        if bool(cv.cv1):
            questions.append("cv1")
        if bool(cv.cv2):
            questions.append("cv2")
        return questions

    def check_stud_cv(self):
        try:
            cv = CV.objects.get(stud=self.stud)
        except CV.DoesNotExist:
            return False
        if not bool(cv.cv1) and not bool(cv.cv2):
            return False
        return True

    def check_stud_credentials(self):
        progjobrel = ProgrammeJobRelation.objects.filter(
            Q(job=self.job, prog__name=self.stud.prog) |
            Q(job=self.job, prog__name=self.stud.minor_prog)
        )
        if not progjobrel:
            return False
        # Check CPI eligibility
        if self.job.cpi_shortlist and self.job.minimum_cpi > self.stud.cpi:
            return False
        # Check BackLog eligibility
        if self.job.backlog_filter and self.job.num_backlogs_allowed < self.stud.active_backlogs:
            return False
        # if already applied, then cannot apply again
        try:
            StudentJobRelation.objects.get(job=self.job, stud=self.stud)
            return False
        except StudentJobRelation.DoesNotExist:
            pass
        return True

    def check_job_credentials(self):
        time_now = timezone.now()
        opening_date_check = self.job.opening_datetime <= time_now
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
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        return True

    def get(self, request, pk):
        self.stud = get_object_or_404(
            Student, id=request.session['student_instance_id'])
        self.job = get_object_or_404(Job, id=pk)
        self.jobrel = get_object_or_404(StudentJobRelation,
                                        stud=self.stud, job=self.job)
        stud_check = self.check_stud_crendentials()
        job_check = self.check_job_credentials()
        if job_check and stud_check:
            self.jobrel.delete()
            return redirect('stud-job-detail', pk=self.job.id)
        else:
            return redirect('stud-job-detail', pk=self.job.id)

    def check_job_credentials(self):
        time_now = timezone.now()
        opening_date_check = self.job.opening_datetime <= time_now
        deadline_check = self.job.application_deadline >= time_now
        approved_check = self.job.approved is True
        return opening_date_check and deadline_check and approved_check

    def check_stud_crendentials(self):
        if self.jobrel.shortlist_init:
            return False
        if self.jobrel.placed_init or self.jobrel.placed_approved:
            return False
        return True


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
            avatar = Avatar.objects.get(
                stud__id=self.request.session['student_instance_id'])
        except Avatar.DoesNotExist:
            avatar = None
        return avatar


class AvatarUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Avatar
    form_class = modelform_factory(
        Avatar,
        fields=['avatar'],
        widgets={
            'avatar': FileInput
        }
    )
    template_name = 'jobportal/Student/avatar_update.html'
    success_url = reverse_lazy('stud-avatar-detail')

    def test_func(self):
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        site_management = SiteManagement.objects.all()[0]
        if site_management.job_stud_photo_allowed is False:
            return False
        return True

    def get_object(self, queryset=None):
        try:
            avatar = Avatar.objects.get(
                stud__id=self.request.session['student_instance_id'])
        except Avatar.DoesNotExist:
            avatar = None
        return avatar


class AvatarCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    form_class = modelform_factory(
        Avatar,
        fields=['avatar'],
        widgets={
            'avatar': FileInput
        }
    )
    template_name = 'jobportal/Student/avatar_create.html'
    success_url = reverse_lazy('stud-avatar-detail')

    def test_func(self):
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        stud_id = self.request.session['student_instance_id']
        if Avatar.objects.filter(stud__id=stud_id).exists():
            return False
        site_management = SiteManagement.objects.all()[0]
        if site_management.job_stud_photo_allowed is False:
            return False
        return True

    def form_valid(self, form):
        avatar = form.save(commit=False)
        avatar.stud = Student.objects.get(
            id=self.request.session['student_instance_id'])
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
            signature = Signature.objects.get(
                stud__id=self.request.session['student_instance_id'])
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
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        site_management = SiteManagement.objects.all()[0]
        if site_management.job_stud_sign_allowed is False:
            return False
        return True

    def form_valid(self, form):
        signature = form.save(commit=False)
        signature.stud = Student.objects.get(
            id=self.request.session['student_instance_id'])
        return super(SignatureCreate, self).form_valid(form)


class SignatureUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Signature
    fields = ['signature']
    template_name = 'jobportal/Student/signature_update.html'
    success_url = reverse_lazy('stud-sign-detail')

    def test_func(self):
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        stud_id = self.request.session['student_instance_id']
        if Signature.objects.filter(stud__id=stud_id).exists():
            return False
        site_management = SiteManagement.objects.all()[0]
        if site_management.job_stud_sign_allowed is False:
            return False
        return True

    def get_object(self, queryset=None):
        try:
            signature = Signature.objects.get(
                stud__id=self.request.session['student_instance_id'])
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
            cv = CV.objects.get(
                stud__id=self.request.session['student_instance_id'])
        except CV.DoesNotExist:
            cv = None
        return cv

    def get_context_data(self, **kwargs):
        context = super(CVDetail, self).get_context_data()
        context['site_management'] = SiteManagement.objects.all()[0]
        return context


class CVCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    form_class = CVForm
    template_name = 'jobportal/Student/cv_create.html'
    success_url = reverse_lazy('stud-cv-detail')

    def test_func(self):
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        site_model = SiteManagement.objects.all()[0]
        now = timezone.now()
        date_passed = site_model.job_student_cv_update_deadline < now
        if date_passed:
            return False
        return True

    def form_valid(self, form):
        cv = form.save(commit=False)
        cv.stud = Student.objects.get(
            id=self.request.session['student_instance_id'])
        return super(CVCreate, self).form_valid(form)


class CVUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('login')
    raise_exception = True
    model = CV
    fields = ['cv1', 'cv2']
    template_name = 'jobportal/Student/cv_update.html'
    success_url = reverse_lazy('stud-cv-detail')

    def test_func(self):
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        site_model = SiteManagement.objects.all()[0]
        now = timezone.now()
        date_passed = site_model.job_student_cv_update_deadline < now
        if date_passed:
            return False
        return True

    def get_object(self, queryset=None):
        try:
            cv = CV.objects.get(
                stud__id=self.request.session['student_instance_id'])
        except CV.DoesNotExist:
            cv = None
        return cv


class DownloadCV(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get(self, request, cvno):
        cv = get_object_or_404(
          CV, stud__id=self.request.session['student_instance_id']
        )
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
