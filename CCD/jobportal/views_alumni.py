from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.decorators import login_required

from .models import Alumni

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
