from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .models import Alumni
from .forms import AlumCVUpload, AlumniProfileForm

ALUM_LOGIN_URL = reverse_lazy('login')


@login_required(login_url=ALUM_LOGIN_URL)
def alum_home(request):
    username = request.user.username
    args = dict(username=username)
    return render(request, 'jobportal/Alumni/home.html', args)


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
