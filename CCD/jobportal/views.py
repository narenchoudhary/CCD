import poplib

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template
from django.utils import timezone
from django.utils.encoding import smart_str
from django.views.generic import (View, ListView, TemplateView, DetailView,
                                  CreateView, UpdateView)

from weasyprint import HTML, CSS

from .models import (UserProfile, Admin, Student, Company, Programme,
                     StudentJobRelation, Event, Job, ProgrammeJobRelation,
                     Avatar, Signature, CV, SiteManagement, Announcement)
from .forms import (LoginForm, EditStudProfileForm, SelectCVForm, CVForm,
                    StudentPlacementConfirm)


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
    """
    View that handles login for all the users.
    """

    # TODO: Create a separate auth.py file and put IMAP login logic there.
    template_name = 'jobportal/login.html'
    server_dict = {
        'dikrong': '202.141.80.13',
        # 'teesta': '202.141.80.12',
        'tamdil': '202.141.80.11',
        # 'naambor': '202.141.80.9',
        'disbang': '202.141.80.10'
    }
    server_port = 995
    next = ""

    def _auth_one_server(self, username, password, server):
        """
        :param username: username
        :param password: password
        :param server: server name, not ip
        :return: login status
        """
        server_ip = self.server_dict.get(str(server).lower())
        try:
            serv = poplib.POP3_SSL(server_ip, self.server_port)
            serv.user(username)
            p_str = serv.pass_(password)
            if 'OK' in p_str:
                serv.quit()
                return True
        except poplib.error_proto:
            serv.quit()
            return False
        except:
            return False
        return False

    def _auth_all_servers(self, username, password):
        """
        :param username: username
        :param password: password
        :return: matching_server, login_status

        login_status == False implies wrong_password.
        """
        for server in self.server_dict.items():
            status = self._auth_one_server(username, password, server[0])
            if status:
                return server[0], True
        return None, False

    def get(self, request):
        form = LoginForm(None)
        self.next = request.GET.get('next', "")
        if request.user.is_authenticated():
            user_profile = UserProfile.objects.get(
                username=request.user.username)
            user_type = user_profile.user_type
            if user_type == 'admin':
                if Admin.objects.filter(user=user_profile).exists():
                    return redirect('admin-home')
            elif user_type == 'company':
                if Company.objects.filter(user=user_profile).exists():
                    return redirect('company-home')
            elif user_type == 'student':
                if Student.objects.filter(user=user_profile).exists():
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
                    if user_type == 'admin':
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
                                form.add_error(None, 'Incorrect password.')
                                return render(request, self.template_name,
                                              dict(form=form))

                        else:
                            form.add_error(None, 'User not active yet.')
                            return render(request, self.template_name,
                                          dict(form=form))
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
                                form.add_error(None, 'Incorrect password.')
                                return render(request, self.template_name,
                                              dict(form=form))
                        else:
                            form.add_error(None, 'User not active yet.')
                            return render(request, self.template_name,
                                          dict(form=form))
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
                                form.add_error(None, 'Incorrect password.')
                                return render(request, self.template_name,
                                              dict(form=form))
                        else:
                            error = 'Your signup request has not been ' \
                                    'approved yet. Please visit again after ' \
                                    'some time.'
                            form.add_error(None, error)
                            return render(request, self.template_name,
                                          dict(form=form))
                    elif user_type == 'student':
                        # fee paid
                        if user_profile.is_active:
                            # check if server is saved
                            if bool(user_profile.login_server):
                                status = self._auth_one_server(
                                    username=username, password=password,
                                    server=user_profile.login_server)
                                # if saved server worked
                                if status:
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
                                        request.session['student_instance_id'] = stud.id
                                        if self.next != "":
                                            return HttpResponseRedirect(self.next)
                                        return redirect('stud-home')
                                # if saved server did not work
                                else:
                                    # try all the servers
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
                                        stud = Student.objects.get(
                                            user=user_profile
                                        )
                                        auth.login(request, user)
                                        request.session[
                                            'student_instance_id'] = stud.id
                                        return redirect('stud-home')
                                    else:
                                        error = 'Wrong password'
                                        form.add_error(None, error)
                                        args = dict(form=form)
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
                                    form.add_error(None, 'Wrong password')
                                    return render(request, self.template_name,
                                                  dict(form=form))

                        else:
                            error = 'User login has been disabled for ' \
                                    'some time. Please try later.'
                            args = dict(form=form, error=error)
                            return render(request, self.template_name, args)
                    elif user_type == 'alumni':
                        pass
                    else:
                        error = 'User has not been activated yet.'
                        args = dict(form=form, error=error)
                        return render(request, self.template_name, args)
                else:
                    form.add_error(None, 'Invalid username')
                    return render(request, self.template_name, dict(form=form))
            else:
                return render(request, self.template_name, dict(form=form))

        else:
            form.add_error(None, 'Please enable cookies and try again.')
            return render(request, self.template_name, dict(form=form))


class Logout(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')

    def test_func(self):
        # check if user exists and is authenticated.
        # TODO: Check if authentication check is really required.
        return self.request.user and self.request.user.is_authenticated()

    def get(self, request):
        auth.logout(request)
        return redirect('index')


class HomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    View class that handles rendering the home page for Student Users
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    template_name = 'jobportal/Student/home.html'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        stud = Student.objects.get(user=self.request.user)
        if stud.placed:
            stud_id = self.request.session['student_instance_id']
            context['jobrel'] = StudentJobRelation.objects.select_related('job').get(
                stud__id=stud_id, placed_approved=True
            )
            if not stud.placed_confirm:
                context['form'] = StudentPlacementConfirm()
        context['stud'] = stud
        return context


class ProfileDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View that handles rendering the profile details for Student users.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
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
    """
    View that handles rendering the profile update form for Student users.
    """
    login_url = reverse_lazy('login')
    raise_exception = True
    form_class = EditStudProfileForm
    template_name = 'jobportal/Student/profile_update.html'
    success_url = reverse_lazy('stud-profile-detail')

    def test_func(self):
        # check if user is student.
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        # TODO: Add internship check here. Currently since FTE students are
        # uploaded on portal, the following check does not check for intern
        # students.
        site_model = SiteManagement.objects.all().first()
        now = timezone.now()
        date_passed = site_model.job_student_profile_update_deadline < now
        if date_passed:
            return False
        return True

    def get_object(self, queryset=None):
        # return logged in user
        return get_object_or_404(
            Student, id=self.request.session['student_instance_id'])


class AllJobList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View class which handles showing all jobs to students.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    template_name = 'jobportal/Student/all_job_list.html'
    context_object_name = 'job_list'

    def test_func(self):
        """
        Test method to limit access based on certain tests.
        :return: True if user is permitted otherwise False
        """
        return self.request.user.user_type == 'student'

    def get_queryset(self):
        """
        Returns queryset of Job instances

        ``select_related`` used for fetching ``company_owner`` in one query.
        Check ``select_related`` documentation.
        https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related

        :return: queryset of Job instances
        """
        return Job.objects.filter(
            approved=True,
            opening_datetime__lte=timezone.now()
        ).select_related('company_owner').order_by('-application_deadline')


class AllJobDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View class which handles showing all jobs to students.
    """
    login_url = reverse_lazy('login')
    raise_exception = True
    model = Job
    template_name = 'jobportal/Student/all_job_detail.html'
    context_object_name = 'job'

    def test_func(self):
        """
        Test method to limit access based on certain tests
        :return: True if user is permitted otherwise False
        """
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        job = get_object_or_404(Job, id=self.kwargs['pk'])
        if job.opening_datetime > timezone.now():
            return False
        return True

    def get_object(self, queryset=None):
        """
        Return Job instance with ``company_owner`` fetched in single query.
        This method was overridden for performance reasons only.
        Check ``select_related`` documentation.
        https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related
        :param queryset: None
        :return: Job instance
        """
        pk = self.kwargs.get('pk')
        return Job.objects.select_related('company_owner').get(pk=pk)

    def get_context_data(self, **kwargs):
        """
        Add Student instance and lists of ProgrammeJobRelation to context.
        :param kwargs: keyword arguments
        :return: context dict
        """
        context = super(AllJobDetail, self).get_context_data(**kwargs)
        context['stud'] = get_object_or_404(
            Student, id=self.request.session['student_instance_id'])
        context['prog_list'] = ProgrammeJobRelation.objects.filter(
            job__id=self.kwargs['pk']
        ).select_related('prog')
        return context


class JobList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Class which handles filtering eligible job for Students.
    """
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    template_name = 'jobportal/Student/job_list.html'
    context_object_name = 'job_list'

    def test_func(self):
        """
        Test method to limit access based on certain tests
        :return: True if user is permitted otherwise False
        """
        return self.request.user.user_type == 'student'

    def get_queryset(self):
        """
        Get eligible Jobs based on student profile.
        :return: queryset of Job
        """
        stud = get_object_or_404(
            Student, id=self.request.session['student_instance_id'])
        try:
            prog = Programme.objects.get(
                year=stud.year, dept=stud.dept, name=stud.prog,
                discipline=stud.discipline, minor_status=False)
        except Programme.DoesNotExist:
            prog = None
        try:
            minor_prog = Programme.objects.get(
                year=stud.minor_year, dept=stud.minor_dept,
                name=stud.minor_prog, discipline=stud.minor_discipline,
                minor_status=True)
        except Programme.DoesNotExist:
            minor_prog = None

        major = ProgrammeJobRelation.objects.filter(prog=prog)
        minor = ProgrammeJobRelation.objects.filter(prog=minor_prog)

        # evil
        if stud.cpi < 5:
            return None

        # blessing
        if stud.ppo:
            return None

        if stud.placed:
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
        ).order_by('-application_deadline')

    def get_context_data(self, **kwargs):
        """
        Get context data with 'stud' added to context.
        :param kwargs: keyword arguments
        :return: context
        """
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
        context['stud'] = get_object_or_404(
            Student, id=self.request.session['student_instance_id'])
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
                minor_status=False)
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
        prog_job_rels = ProgrammeJobRelation.objects.filter(
            Q(job=self.job, prog=self.prog) |
            Q(job=self.job, prog=self.minor_prog)
        )
        if not prog_job_rels:
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
    # render login page instead of raising 403 error
    raise_exception = False
    template_name = 'jobportal/Student/jobrel_list.html'
    context_object_name = 'jobrel_list'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_queryset(self):
        return StudentJobRelation.objects.filter(
            stud__id=self.request.session['student_instance_id'],
            is_debarred=False
        ).order_by('-creation_datetime').select_related('job')


class JobRelDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    model = ProgrammeJobRelation
    template_name = 'jobportal/Student/jobrel_detail.html'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return StudentJobRelation.objects.select_related('job').get(id=pk)


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

        stud_id = self.request.session['student_instance_id']
        self.stud = get_object_or_404(Student, id=stud_id)
        self.job = get_object_or_404(Job, id=self.kwargs['pk'])

        if self.stud.placed:
            return False

        stud_cv_check = self.check_stud_cv()
        if not stud_cv_check:
            return False
        stud_check = self.check_stud_credentials()
        if not stud_check:
            return False
        job_check = self.check_job_credentials()
        if not job_check:
            return False

        return True

    def get(self, request, pk):
        form = SelectCVForm(extra=self.get_questions())
        return render(request, self.template, dict(form=form, job=self.job))

    def post(self, request, pk):
        form = SelectCVForm(request.POST, extra=self.get_questions())
        if form.is_valid():
            jobrel = StudentJobRelation(stud=self.stud, job=self.job)
            for (question, answer) in form.extra_answers():
                setattr(jobrel, str(question).lower(), answer)
            jobrel.save()
            return redirect('stud-job-detail', pk=self.job.id)
        else:
            context = dict(form=form, job=self.job)
            return render(request, self.template, context)

    def get_questions(self):
        """
        Get list of CVs uploaded by student.
        :return: list of CVs
        """
        cv = get_object_or_404(CV, stud=self.stud)
        questions = []
        if bool(cv.cv1):
            questions.append("cv1")
        if bool(cv.cv2):
            questions.append("cv2")
        return questions

    def check_stud_cv(self):
        """
        Check if student has uploaded any CV
        :return: True if student has uploaded at least one CV otherwise False
        """
        try:
            cv = CV.objects.get(stud=self.stud)
        except CV.DoesNotExist:
            return False
        return bool(cv.cv1) or bool(cv.cv2)

    def check_stud_credentials(self):
        """
        Check if Student is eligible for applying for the Job.
        :return: True if student is eligible otherwise False
        """
        progjobrel = ProgrammeJobRelation.objects.filter(
            Q(job=self.job, prog__name=self.stud.prog) |
            Q(job=self.job, prog__name=self.stud.minor_prog)
        ).exists()
        if not progjobrel:
            return False
        # Check CPI eligibility
        if self.job.cpi_shortlist and self.job.minimum_cpi > self.stud.cpi:
            return False
        # Check BackLog eligibility
        if self.job.backlog_filter and self.job.num_backlogs_allowed < self.stud.active_backlogs:
            return False
        # if debarred or already applied, then cannot apply again
        try:
            StudentJobRelation.objects.get(job=self.job, stud=self.stud)
            return False
        except StudentJobRelation.DoesNotExist:
            pass
        # Otherwise
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


class AvatarDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    # render login page instead of raising 403 error
    raise_exception = False
    model = Avatar
    template_name = 'jobportal/Student/avatar_detail.html'
    context_object_name = 'avatar'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        """
        Return Avatar object related to logged in Student user.

        `select_related`` used for fetching ``stud`` in one query.
        Check ``select_related`` documentation.
        https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related

        :param queryset: None
        :return: Avatar instance
        """
        try:
            avatar = Avatar.objects.select_related('stud').get(
                stud__id=self.request.session['student_instance_id'])
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
    # raise 403 error instead of rendering login page
    raise_exception = True
    model = Avatar
    fields = ['avatar']
    template_name = 'jobportal/Student/avatar_create.html'
    success_url = reverse_lazy('stud-avatar-detail')

    def test_func(self):
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        # check if Avatar instance already exists
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
    # render login page instead of raising 403 error
    raise_exception = False
    model = Signature
    template_name = 'jobportal/Student/signature_detail.html'
    context_object_name = 'signature'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        """
        Return Signature object related to logged in Student user.

        `select_related`` used for fetching ``stud`` in one query.
        Check ``select_related`` documentation.
        https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related

        :param queryset: None
        :return: Signature instance
        """
        try:
            signature = Signature.objects.select_related('stud').get(
                stud__id=self.request.session['student_instance_id'])
        except Signature.DoesNotExist:
            signature = None
        return signature


class SignatureCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    # raise 403 error instead of rendering login page
    raise_exception = True
    model = Signature
    fields = ['signature']
    template_name = 'jobportal/Student/signature_create.html'
    success_url = reverse_lazy('stud-sign-detail')

    def test_func(self):
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
            return False
        # check if Signature instance already exists
        stud_id = self.request.session['student_instance_id']
        if Signature.objects.filter(stud__id=stud_id).exists():
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
    # raise 403 error instead of rendering login page
    raise_exception = True
    model = Signature
    fields = ['signature']
    template_name = 'jobportal/Student/signature_update.html'
    success_url = reverse_lazy('stud-sign-detail')

    def test_func(self):
        is_stud = self.request.user.user_type == 'student'
        if not is_stud:
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
    # render login page instead of raising 403 error
    raise_exception = False
    model = CV
    template_name = 'jobportal/Student/cv_detail.html'
    context_object_name = 'cv'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        try:
            cv = CV.objects.select_related('stud').get(
                stud__id=self.request.session['student_instance_id'])
        except CV.DoesNotExist:
            cv = None
        return cv

    def get_context_data(self, **kwargs):
        context = super(CVDetail, self).get_context_data()
        context['site_management'] = SiteManagement.objects.all().first()
        return context


class CVCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('login')
    # raise 403 error instead of rendering login page
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
    # raise 403 error instead of rendering login page
    raise_exception = True
    form_class = CVForm
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


class AnnouncementList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    raise_exception = False
    template_name = 'jobportal/Student/announcement_list.html'
    context_object_name = 'announcement_list'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_queryset(self):
        return Announcement.objects.filter(
            hide=False).order_by('-last_updated')


class DownloadDeclaration(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'jobportal/Student/declaration.html'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get(self, request):
        html_template = get_template(self.template_name)
        stud = get_object_or_404(
            Student, id=self.request.session['student_instance_id'])
        rendered_html = html_template.render(
            RequestContext(request, dict(stud=stud))
        )
        pdf_file = HTML(
            string=rendered_html, base_url=request.build_absolute_uri()
        ).write_pdf(
            stylesheets=[CSS(string='body { font-family: "Helvetica" }')])
        http_response = HttpResponse(pdf_file, content_type='application/pdf')
        http_response['Content-Disposition'] = 'filename="declaration.pdf"'
        return http_response


class StudentPlacementFormHandler(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    raise_exception = False
    template_name = 'jobportal/Student/home.html'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get(self, request):
        return redirect('stud-home')

    def post(self, request):
        form = StudentPlacementConfirm(request.POST)
        if form.is_valid():
            confirm = form.cleaned_data['confirm']
            if confirm:
                stud = Student.objects.get(id=request.session['student_instance_id'])
                stud.placed_confirm = True
                stud.save()
                return redirect('stud-home')
            else:
                return redirect('stud-home')
        else:
            return redirect('stud-home')
