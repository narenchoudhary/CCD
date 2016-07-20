from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.utils import timezone
from jobportal.models import Company, Alumni
from .models import AlumJob, AlumJobRelation
from .forms import CompanyAddAlumJob, AdminEditAlumJob
from datetime import datetime, timedelta


def company_add_job(request):
    company_instance = get_object_or_404(Company, id=request.session['company_instance_id'])
    form = CompanyAddAlumJob(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            job_instance = form.save(commit=False)
            job_instance.company_owner = company_instance
            job_instance.posted_on = datetime.now()
            job_instance.opening_date = datetime.now() + timedelta(days=15)
            job_instance.closing_date = datetime.now() + timedelta(days=30)
            job_instance.save()
            return redirect('alumnijobs:rec_all_alum_jobs')
        else:
            args = dict(form=form)
            return render(request, 'alumnijobs/company/add_job.html', args)
    else:
        args = dict(form=form)
        return render(request, 'alumnijobs/company/add_job.html', args)


def company_all_alum_jobs(request):
    company_instance = get_object_or_404(Company, id=request.session['company_instance_id'])
    job_list = AlumJob.objects.all().filter(company_owner=company_instance)
    args = dict(job_list=job_list)
    return render(request, 'alumnijobs/company/all_jobs.html', args)


def company_alum_job_details(request, jobid):
    job = AlumJob.objects.get(id=jobid)
    args = dict(job=job)
    return render(request, 'alumnijobs/company/job_details.html', args)


def company_edit_alum_job(request, jobid):
    job_instance = get_object_or_404(AlumJob, id=jobid)
    form = CompanyAddAlumJob(request.POST or None, instance=job_instance)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('alumnijobs:rec_alum_job_details', jobid=jobid)
        else:
            args = dict(job=job_instance, form=form)
            return render(request, 'alumnijobs/company/edit_job.html', args)
    else:
        args = dict(job=job_instance, form=form)
        return render(request, 'alumnijobs/company/edit_job.html', args)


def company_alum_job_candidates(request, jobid):
    job = get_object_or_404(AlumJob, id=jobid)
    rel_list = AlumJobRelation.objects.all().filter(job=job)
    args = dict(rel_list=rel_list, job=job)
    return render(request, 'alumnijobs/company/all_candidates.html', args)


def alum_all_jobs(request):
    job_list = AlumJob.objects.all()
    args = dict(job_list=job_list)
    return render(request, 'alumnijobs/alumni/all_jobs.html', args)


def alum_alum_job_details(request, jobid):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    job = get_object_or_404(AlumJob, id=jobid)
    cv = False if not bool(alum_instance.cv) else True
    datetime_now = timezone.make_aware(datetime.now())
    deadline_passed = True if job.closing_date < datetime_now else False
    job_open = True if job.opening_date < datetime_now else False
    try:
        alum_rel = AlumJobRelation.objects.get(job=job, alum=alum_instance)
    except AlumJobRelation.DoesNotExist:
        alum_rel = None
    args = dict(cv=cv, job=job, alum_rel=alum_rel, deadline_passed=deadline_passed, job_open=job_open)
    return render(request, 'alumnijobs/alumni/job_details.html', args)


def alum_alum_job_apply(request, jobid):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    job = get_object_or_404(AlumJob, id=jobid)
    try:
        alum_rel = AlumJobRelation.objects.get(job=job, alum=alum_instance)
    except AlumJobRelation.DoesNotExist:
        cv = True if bool(alum_instance.cv) else False
        datetime_now = timezone.make_aware(datetime.now())
        deadline_passed = True if job.closing_date < datetime_now else False
        job_open = True if job.opening_date < datetime_now else False
        if job_open and not deadline_passed and cv:
            alum_rel = AlumJobRelation.objects.create(job=job, alum=alum_instance)
    return redirect('alumnijobs:alum_alum_job_details', jobid=jobid)


def alum_alum_job_deapply(request, jobid):
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    job = get_object_or_404(AlumJob, id=jobid)
    try:
        datetime_now = timezone.make_aware(datetime.now())
        deadline_passed = True if job.closing_date < datetime_now else False
        if not deadline_passed:
            alum_rel = AlumJobRelation.objects.get(job=job, alum=alum_instance)
            alum_rel.delete()
    except AlumJobRelation.DoesNotExist:
        pass
    return redirect('alumnijobs:alum_alum_job_details', jobid=jobid)


def admin_all_alum_jobs(request):
    job_list = AlumJob.objects.all()
    args = dict(job_list=job_list)
    return render(request, 'alumnijobs/admin/all_jobs.html', args)


def admin_alum_job_details(request, jobid):
    job_instance = get_object_or_404(AlumJob, id=jobid)
    args = dict(job_instance=job_instance)
    return render(request, 'alumnijobs/admin/job_details.html', args)


def admin_edit_alum_job(request, jobid):
    job_instance = get_object_or_404(AlumJob, id=jobid)
    form = AdminEditAlumJob(request.POST or None, instance=job_instance)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('alumnijobs:admin_alum_job_details', jobid=jobid)
        else:
            args = dict(form=form, job=job_instance)
            return render(request, 'alumnijobs/admin/edit_job.html', args)
    else:
        args = dict(form=form, job=job_instance)
        return render(request, 'alumnijobs/admin/edit_job.html', args)
