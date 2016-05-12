from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.exceptions import *
from django.contrib.auth.models import User
from .models import UserProfile, Student, Alumni, Job, StudentJobRelation
from .forms import AlumCVUpload, AlumniProfileForm, JobEditForm

ALUM_LOGIN_URL = reverse_lazy('login')


@login_required(login_url=ALUM_LOGIN_URL)
def alum_logout(request):
    """
    Logout Alumni.
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    # logout user
    auth.logout(request)
    return render(request, 'jobportal/logout.html')


@login_required(login_url=ALUM_LOGIN_URL)
def alum_home(request):
    """
    Alumni home.
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    username = request.user.username
    args = {'username': username}
    return render(request, 'jobportal/Alumni/home.html', args)


@login_required(login_url=ALUM_LOGIN_URL)
def view_jobs(request):
    """
    View jobs added by Alumni.
    :param request: HttpRequest object
    :return: HttpResponse object
    """
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    job_list = Job.objects.all().filter(alum_owner=alum_instance)
    args = {}
    args.update(csrf(request))
    args['job_list'] = job_list
    return render(request, 'jobportal/Alumni/postedjobs.html', args)


# Add a new job/internship entry
@login_required(login_url=ALUM_LOGIN_URL)
def alum_add_job(request):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    if request.method == "POST":
        job_add_form = JobEditForm(request.POST)
        if job_add_form.is_valid():
            job_instance = Job(alum_owner=alum_instance,
                               posted_by_alumnus=True,
                               posted_by_company=False,
                               description=job_add_form.cleaned_data['description'],
                               designation=job_add_form.cleaned_data['designation'],
                               open_for_alum=job_add_form.cleaned_data['open_for_alum'],
                               cpi_shortlist=job_add_form.cleaned_data['cpi_shortlist'],
                               percentage_x=job_add_form.cleaned_data['percentage_x'],
                               percentage_xii=job_add_form.cleaned_data['percentage_xii'],
                               other_requirements=job_add_form.cleaned_data['other_requirements'],
                               num_openings=job_add_form.cleaned_data['num_openings'],
                               currency=job_add_form.cleaned_data['currency'],
                               ctc_btech=job_add_form.cleaned_data['ctc_btech'],
                               ctc_mtech=job_add_form.cleaned_data['ctc_mtech'],
                               ctc_ma=job_add_form.cleaned_data['ctc_ma'],
                               ctc_msc=job_add_form.cleaned_data['ctc_msc'],
                               ctc_phd=job_add_form.cleaned_data['ctc_phd'],
                               gross_btech=job_add_form.cleaned_data['gross_btech'],
                               gross_mtech=job_add_form.cleaned_data['gross_mtech'],
                               gross_ma=job_add_form.cleaned_data['gross_ma'],
                               gross_msc=job_add_form.cleaned_data['gross_msc'],
                               gross_phd=job_add_form.cleaned_data['gross_phd'],
                               take_home_during_training=job_add_form.cleaned_data['take_home_during_training'],
                               take_home_after_training=job_add_form.cleaned_data['take_home_after_training'],
                               bonus=job_add_form.cleaned_data['bonus'],
                               bond=job_add_form.cleaned_data['bond'],
                               bond_details=job_add_form.cleaned_data['bond_details'],
                               profile_name=job_add_form.cleaned_data['profile_name'],
                               posted_on=datetime.now(),
                               last_updated=datetime.now(),
                               )
            job_instance.save()

            dept_list = job_add_form.cleaned_data['dept']
            current_year_list = job_add_form.cleaned_data['current_year']
            prog_list = job_add_form.cleaned_data['prog']

            for adept in dept_list:
                job_instance.dept.add(adept)
            for acurrent_year in current_year_list:
                job_instance.current_year.add(acurrent_year)
            for aprog in prog_list:
                job_instance.prog.add(aprog)

            return redirect('alumviewjobs')

        else:
            args = {}
            args.update(csrf(request))
            args['add_job_form'] = job_add_form
            return render(request, 'jobportal/Alumni/postjob.html', args)
    else:
        args = {}
        args.update(csrf(request))
        args['add_job_form'] = JobEditForm()
        return render(request, 'jobportal/Alumni/postjob.html', args)


# Edit an existing job/internship entry
@login_required(login_url=ALUM_LOGIN_URL)
def alum_edit_job(request, jobid):
    job = Job.objects.get(id=jobid)
    if request.method == "POST":
        job_add_form = JobEditForm(request.POST)
        if job_add_form.is_valid():
            job.description = job_add_form.cleaned_data['description']
            job.designation = job_add_form.cleaned_data['designation']
            job.open_for_alum = job_add_form.cleaned_data['open_for_alum']
            job.cpi_shortlist = job_add_form.cleaned_data['cpi_shortlist']
            job.minimum_cpi = job_add_form.cleaned_data['minimum_cpi']
            job.percentage_x = job_add_form.cleaned_data['percentage_x']
            job.percentage_xii = job_add_form.cleaned_data['percentage_xii']
            job.other_requirements = job_add_form.cleaned_data['other_requirements']
            job.num_openings = job_add_form.cleaned_data['num_openings']
            job.currency = job_add_form.cleaned_data['currency']
            job.ctc_btech = job_add_form.cleaned_data['ctc_btech']
            job.ctc_mtech = job_add_form.cleaned_data['ctc_mtech']
            job.ctc_ma = job_add_form.cleaned_data['ctc_ma']
            job.ctc_msc = job_add_form.cleaned_data['ctc_msc']
            job.ctc_phd = job_add_form.cleaned_data['ctc_phd']
            job.gross_btech = job_add_form.cleaned_data['gross_btech']
            job.gross_mtech = job_add_form.cleaned_data['gross_mtech']
            job.gross_ma = job_add_form.cleaned_data['gross_ma']
            job.gross_msc = job_add_form.cleaned_data['gross_msc']
            job.gross_phd = job_add_form.cleaned_data['gross_phd']
            job.take_home_during_training = job_add_form.cleaned_data['take_home_during_training']
            job.take_home_after_training = job_add_form.cleaned_data['take_home_after_training']
            job.bonus = job_add_form.cleaned_data['bonus']
            job.bond = job_add_form.cleaned_data['bond']
            job.bond_details = job_add_form.cleaned_data['bond_details']
            job.profile_name = job_add_form.cleaned_data['profile_name']
            job.last_updated = datetime.now()
            job.save()

            dept_list = job_add_form.cleaned_data['dept']
            current_year_list = job_add_form.cleaned_data['current_year']
            prog_list = job_add_form.cleaned_data['prog']

            job.dept.clear()
            job.current_year.clear()
            job.prog.clear()

            for adept in dept_list:
                job.dept.add(adept)
            for acurrent_year in current_year_list:
                job.current_year.add(acurrent_year)
            for aprog in prog_list:
                job.prog.add(aprog)

            return redirect('alumviewjobs')
        else:
            args = {}
            args.update(csrf(request))
            args['edit_job_form'] = job_add_form
            args['job'] = job
            return render(request, 'jobportal/Alumni/editjob.html', args)

    else:
        args = {}
        args.update(csrf(request))
        args['edit_job_form'] = JobEditForm(initial={
            'description': job.description,
            'designation': job.designation,
            'open_for_alum': job.open_for_alum,
            'cpi_shortlist': job.cpi_shortlist,
            'minimum_cpi': job.minimum_cpi,
            'percentage_x': job.percentage_x,
            'percentage_xii': job.percentage_xii,
            'num_openings': job.num_openings,
            'other_requirements': job.other_requirements,
            'currency': job.currency,
            'ctc_btech': job.ctc_btech,
            'ctc_mtech': job.ctc_mtech,
            'ctc_ma': job.ctc_msc,
            'ctc_msc': job.ctc_ma,
            'ctc_phd': job.ctc_phd,
            'gross_btech': job.gross_btech,
            'gross_mtech': job.gross_mtech,
            'gross_ma': job.gross_ma,
            'gross_msc': job.gross_msc,
            'gross_phd': job.gross_phd,
            'take_home_during_training': job.take_home_during_training,
            'take_home_after_training': job.take_home_after_training,
            'bonus': job.bonus,
            'bond': job.bond,
            'bond_details': job.bond_details,
            'profile_name': job.profile_name,
            'prog': job.prog.all(),
            'dept': job.dept.all(),
            'current_year': job.current_year.all()
        })
        args['job'] = job
        return render(request, 'jobportal/Alumni/editjob.html', args)


# Delete an existing job/internship entry
@login_required(login_url=ALUM_LOGIN_URL)
def alum_del_job(request, jobid):
    job = get_object_or_404(Job, id=jobid)
    job.delete()
    return redirect('alumviewjobs')


# Candidates for a job; both alumni and students
@login_required(login_url=ALUM_LOGIN_URL)
def alum_candidates(request, jobid):
    job = get_object_or_404(Job, id=jobid)
    args = {'jobid': job.id,
            'stud_list': job.students.all(),
            'alum_list': job.alums.all()
            }
    return render(request, 'jobportal/Alumni/candidates.html', args)


# Alumni Job application related Views
# Alumni: Apply for a job
@login_required(login_url=ALUM_LOGIN_URL)
def alum_apply(request, jobid):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    job_instance = get_object_or_404(Job, id=jobid)
    # relation_instance = AlumJobRelation(
    #     alum=alum_instance,
    #     job=job_instance,
    #     shortlist_status=False
    # )
    # relation_instance.save()
    return redirect('alum_jobdetails', jobid=jobid)


# Alumni: Remove a job application
@login_required(login_url=ALUM_LOGIN_URL)
def alum_deapply(request, jobid):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    job_instance = get_object_or_404(Job, id=jobid)
    # relation_instance = get_object_or_404(AlumJobRelation, alum=alum_instance, job=job_instance)
    # relation_instance.delete()
    return redirect('alum_jobdetails', jobid=jobid)


# Alumni: Jobs available for application
@login_required(login_url=ALUM_LOGIN_URL)
def jobs_availabe(request):
    jobs = Job.objects.filter(open_for_alum=True)
    args = {'job_list': jobs}
    return render(request, 'jobportal/Alumni/availablejobs.html', args)


# Alumni: Jobs applied for
@login_required(login_url=ALUM_LOGIN_URL)
def alum_jobsappliedfor(request):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    job_list = alum_instance.job_set.all()
    args = {'job_list': job_list}
    return render(request, 'jobportal/Alumni/appliedfor.html', args)


# Alumni: Job details
@login_required(login_url=ALUM_LOGIN_URL)
def alum_jobdetails(request, jobid):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    job_instance = get_object_or_404(Job, id=jobid)
    args = {'job_instance': job_instance}
    # try:
    #     relation_instance = AlumJobRelation.objects.get(alum=alum_instance, job=job_instance)
    #     args['relation_instance'] = relation_instance
    # except ObjectDoesNotExist:
    #     args['relation_instance'] = None
    args['relation_instance'] = None
    return render(request, 'jobportal/Alumni/jobdetails.html', args)


# Student Job relation Views
@login_required(login_url=ALUM_LOGIN_URL)
def job_stud_relation(request, jobid, studid):
    stud_instance = get_object_or_404(Student, id=studid)
    job_instance = get_object_or_404(Job, id=jobid)
    relation_instance = get_object_or_404(StudentJobRelation, stud=stud_instance, job=job_instance)
    args = {'relation_instance': relation_instance,
            'stud_instance': stud_instance,
            'job_instance': job_instance
            }
    return render(request, 'jobportal/Alumni/jobactions.html', args)


# Student Shortlist
@login_required(login_url=ALUM_LOGIN_URL)
def job_shortlist(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.shortlist_status = True
    relation_instance.save()
    return redirect("alum_jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


# Student Unshortlist
@login_required(login_url=ALUM_LOGIN_URL)
def job_unshortlist(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.shortlist_status = False
    relation_instance.save()
    return redirect("alum_jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


# Student Place
@login_required(login_url=ALUM_LOGIN_URL)
def job_place(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.placed_init = True
    relation_instance.save()
    return redirect("alum_jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


# Student Unplace
@login_required(login_url=ALUM_LOGIN_URL)
def job_unplace(request, relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    relation_instance.placed_init = False
    relation_instance.save()
    return redirect("alum_jobaction", jobid=relation_instance.job.id, studid=relation_instance.stud.id)


@login_required(login_url=ALUM_LOGIN_URL)
def view_profile(request):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    args = dict(alum_instance=alum_instance)
    return render(request, 'jobportal/Alumni/profile.html', args)


@login_required(login_url=ALUM_LOGIN_URL)
def edit_profile(request):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    form = AlumniProfileForm(request.POST or None, instance=alum_instance)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('alum_view_profile')
        else:
            args = dict(form=form, alum_instance=alum_instance)
            return render(request, 'jobportal/Alumni/edit_profile.html', args)
    else:
        args = dict(form=form, alum_instance=alum_instance)
        return render(request, 'jobportal/Alumni/edit_profile.html', args)


@login_required(login_url=ALUM_LOGIN_URL)
def upload_cv(request):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    form = AlumCVUpload(request.POST or None, request.FILES or None, instance=alum_instance)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('alum_cv_upload')
        else:
            args = dict(form=form, alum_instance=alum_instance)
            return render(request, 'jobportal/Alumni/uploadcv.html', args)
    else:
        args = dict(form=form, alum_instance=alum_instance)
        return render(request, 'jobportal/Alumni/uploadcv.html', args)
