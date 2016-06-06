from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, Http404
from models import Company, Job, StudentJobRelation
import csv

from views_admin import ADMIN_LOGIN_URL

from .forms import RequestEventForm
from .models import Event, Alumni, Student


def candidates_stud_csv(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    stud_candidates = get_list_or_404(StudentJobRelation, job=job_instance)
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename = ' + job_instance.designation + '.csv'

    writer = csv.writer(response)
    writer.writerow(
        ['first name', 'middle_name', 'last_name', 'roll_no', 'Department', 'Year', 'Shortlisted', 'Placed'])
    for candidate in stud_candidates:
        writer.writerow(
            [
                candidate.stud.first_name,
                candidate.stud.middle_name,
                candidate.stud.last_name,
                candidate.stud.roll_no,
                candidate.stud.dept,
                candidate.stud.year,
                candidate.shortlist_status,
                candidate.placed_init
            ]
        )
    return response


@login_required(login_url=ADMIN_LOGIN_URL)
def companies_csv(request):
    companies = get_list_or_404(Company)
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename = all_companies.csv'

    writer = csv.writer(response)
    writer.writerow(
        ['Name', 'Description', 'Postal Address', 'Website', 'Organization Type', 'Industry Sector', 'Head HR Name',
         'Head HR Mobile'
         'Head HR Email', 'Head HR Designation', 'Head HR Fax', 'First HR Name', 'First HR Mobile', 'First HR Email',
         'First HR Designation', 'First HR Fax'])
    for company in companies:
        writer.writerow(
            [
                company.company_name,
                company.description,
                company.postal_address,
                company.website,
                company.organization_type,
                company.industry_sector,
                company.head_hr_name,
                company.head_hr_mobile,
                company.head_hr_email,
                company.head_hr_designation,
                company.head_hr_fax,
                company.first_hr_name,
                company.first_hr_mobile,
                company.first_hr_email,
                company.first_hr_designation,
                company.first_hr_fax
            ]
        )

    return response


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


@login_required(login_url=reverse_lazy('login'))
def eventlist(request):
    event_list = Event.objects.filter(finalised=True)
    args = {'event_list': event_list}
    return render(request, 'jobportal/Student/event.html', args)


@login_required(login_url=reverse_lazy('login'))
def view_avatar(request):
    student_instance = Student.objects.get(id=request.session['student_instance_id'])
    args = {'student_instance': student_instance}
    return render(request, 'jobportal/Student/viewavatar.html', args)
