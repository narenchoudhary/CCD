from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, Http404
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from datetime import datetime
from reportlab.pdfgen import canvas
from io import BytesIO

from .models import Company, Student, Alumni, Admin, StudentJobRelation, User, Event, Job, \
    ProgrammeJobRelation, UserProfile
from .forms import LoginForm, StudCVForm, EditStudProfileForm, RequestEventForm, SelectCVForm, AvatarSignForm

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
            # authenticate
            user = auth.authenticate(username=username, password=password)
            # user exists
            if user is not None:
                current_user = User.objects.get(username=username)
                user_profile = UserProfile.objects.get(user=current_user)
                if user_profile.login_type == 'Current Student':
                    auth.login(request, user)
                    student_instance = Student.objects.get(user=user_profile)
                    request.session['student_instance_id'] = student_instance.id
                    request.session['user_type'] = 'Student'
                    return redirect('stud_home')
                elif user_profile.login_type == 'Company':
                    auth.login(request, user)
                    company_instance = Company.objects.get(user=user_profile)
                    request.session['company_instance_id'] = company_instance.id
                    request.session['user_type'] = 'Company'
                    return redirect('companyhome')
                elif user_profile.login_type == 'Alumni':
                    auth.login(request, user)
                    alum_instance = Alumni.objects.get(user=user_profile)
                    request.session['alum_instance_id'] = alum_instance.id
                    request.session['user_type'] = 'Alumni'
                    return redirect('alum_home')
                elif user_profile.login_type == 'Admin':
                    auth.login(request, user)
                    admin_instance = Admin.objects.get(user=user_profile)
                    # set session variables
                    request.session['admin_instance_id'] = admin_instance.id
                    request.session['user_type'] = 'Admin'
                    return redirect('admin_home')
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


@login_required(login_url=STUD_LOGIN_URL)
def stud_logout(request):
    auth.logout(request)
    return render(request, 'jobportal/logout.html')


@login_required(login_url=STUD_LOGIN_URL)
def stud_home(request):
    try:
        student_instance = Student.objects.get(id=request.session['student_instance_id'])
    except:
        raise Http404("Error 404")
    args = dict(stud=student_instance)
    return render(request, 'jobportal/Student/stud_home.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def edit_stud_profile(request):
    student_instance = Student.objects.get(id=request.session['student_instance_id'])
    edit_stud_form_data = EditStudProfileForm(request.POST or None, instance=student_instance)
    if request.method == "POST":
        if edit_stud_form_data.is_valid():
            stud = edit_stud_form_data.save(commit=False)
            stud.save()
            return redirect('stud_home')
        else:
            args = dict(edit_stud_profile_form=edit_stud_form_data)
            return render(request, 'jobportal/Student/editstudprofile.html', args)
    else:
        args = dict(edit_stud_profile_form=edit_stud_form_data)
        return render(request, 'jobportal/Student/editstudprofile.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def stud_viewjobs(request):
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    stud_prog = student_instance.prog
    job_list = set([e.job for e in ProgrammeJobRelation.objects.filter(prog=stud_prog)])
    return render(request, 'jobportal/Student/studjobs.html', dict(job_list=job_list, stud_prog=stud_prog))


@login_required(login_url=STUD_LOGIN_URL)
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


@login_required(login_url=STUD_LOGIN_URL)
def stud_deapplyjob(request, jobid):
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    job_instance = Job.objects.get(id=jobid)
    relation_instance = get_object_or_404(StudentJobRelation, stud=student_instance, job=job_instance)
    relation_instance.delete()
    return redirect('jobdetails', jobid=jobid)


@login_required(login_url=STUD_LOGIN_URL)
def stud_jobsappliedfor(request):
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    job_list = [e.job for e in StudentJobRelation.objects.filter(stud=student_instance)]
    args = {'job_list': job_list}
    return render(request, 'jobportal/Student/appliedfor.html', args)


@login_required(login_url=STUD_LOGIN_URL)
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


@login_required(login_url=STUD_LOGIN_URL)
def view_cvs(request):
    student_instance = Student.objects.get(id=request.session['student_instance_id'])
    args = {'student_instance': student_instance}
    return render(request, 'jobportal/Student/viewcvs.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def cv_upload(request):
    stud_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    if request.method == "POST":
        cv_data = StudCVForm(request.POST, request.FILES or None)
        if cv_data.is_valid():
            stud_instance.cv1 = cv_data.cleaned_data['cv1']
            stud_instance.cv2 = cv_data.cleaned_data['cv2']
            stud_instance.save()
            return redirect("viewcvs")
        else:
            args = {'cv_upload_form': cv_data}
            return render(request, 'jobportal/Student/cvupload.html', args)
    else:
        args = {'cv_upload_form': StudCVForm(initial={
            'cv1': stud_instance.cv1,
            'cv2': stud_instance.cv2
        })}
        return render(request, 'jobportal/Student/cvupload.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def del_cv(request, cvno):
    stud_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    if str(cvno) == "1":
        stud_instance.cv1.delete()
        stud_instance.save()
    if str(cvno) == "2":
        stud_instance.cv2.delete()
        stud_instance.save()
    return redirect("viewcvs")


def requestevent(request):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    if request.method == 'POST':
        event_form_data = RequestEventForm(request.POST)
        if event_form_data.is_valid():
            event_instance = Event(
                alum_owner=alum_instance,
                title=event_form_data.cleaned_data['title'],
                date1=event_form_data.cleaned_data['date1'],
                date2=event_form_data.cleaned_data['date2'],
                date3=event_form_data.cleaned_data['date3']
            )
            event_instance.save()
            return redirect('alum_home')
        else:
            args = {'event_form': event_form_data}
            return render(request, 'jobportal/Alumni/requestevent.html', args)
    else:
        args = {}
        args.update(csrf(request))
        args['event_form'] = RequestEventForm()

        return render(request, 'jobportal/Alumni/requestevent.html', args)


def eventsandstatus(request):
    alum_instance = Alumni.objects.get(id=request.session['alum_instance_id'])
    args = {'event_list': Event.objects.filter(alum_owner=alum_instance)}
    return render(request, 'jobportal/Alumni/eventsandstatus.html', args)


# ---------------------
# Experiments
# ---------------------

@login_required
def stud_pdf(request):
    response = HttpResponse(content_type="application/pdf")

    response['Content-Disposition'] = 'filename = "student_jobs.pdf"'

    byte_buffer = BytesIO()

    p = canvas.Canvas(byte_buffer)

    p.drawString(50, 50, 'Hello World')

    p.showPage()
    p.save()

    pdf = byte_buffer.getvalue()
    byte_buffer.close()
    response.write(pdf)

    return response


"""

Company view

"""


@login_required(login_url=COMPANY_LOGIN_URL)
def company_requestevent(request):
    try:
        company_instance = Company.objects.get(id=request.session['company_instance_id'])
    except:
        raise Http404("404 Error.")
    if request.method == 'POST':
        event_form_data = RequestEventForm(request.POST)

        if event_form_data.is_valid():
            event_instance = Event(
                company_owner=company_instance,
                title=event_form_data.cleaned_data['title'],
                date1=event_form_data.cleaned_data['date1'],
                date2=event_form_data.cleaned_data['date2'],
                date3=event_form_data.cleaned_data['date3']
            )
            event_instance.save()
            return redirect('companyhome')
        else:
            args = {'event_form': event_form_data}
            return render(request, 'jobportal/Company/requestevent.html', args)
    else:
        args = {}
        args.update(csrf(request))
        args['event_form'] = RequestEventForm()
        return render(request, 'jobportal/Company/requestevent.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def eventlist(request):
    event_list = Event.objects.filter(finalised=True)
    args = {'event_list': event_list}
    return render(request, 'jobportal/Student/event.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def view_avatar(request):
    student_instance = Student.objects.get(id=request.session['student_instance_id'])
    args = {'student_instance': student_instance}
    return render(request, 'jobportal/Student/viewavatar.html', args)


@login_required(login_url=STUD_LOGIN_URL)
def upload_avatar_sign(request):
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    avatar_sign_form = AvatarSignForm(request.POST or None, request.FILES or None, instance=student_instance)
    if request.method == 'POST':
        if avatar_sign_form.is_valid():
            print avatar_sign_form.cleaned_data['avatar']
            print avatar_sign_form.cleaned_data['signature']
            avatar_sign_form.save()
            return render(request, 'jobportal/Student/stud_home.html', dict(stud=student_instance))
        else:
            args = dict(avatar_sign_form=avatar_sign_form, stud=student_instance)
            return render(request, 'jobportal/Student/upload_avatar_sign.html', args)
    else:
        args = dict(avatar_sign_form=avatar_sign_form, stud=student_instance)
        return render(request, 'jobportal/Student/upload_avatar_sign.html', args)
