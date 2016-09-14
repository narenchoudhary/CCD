from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from jobportal.models import Alumni, Student
from .models import StudentProposalRelation, ResearchProposal
from .forms import AddProposal, EditProposal, StudApply, ReportForm

alum_login_url = reverse_lazy('jobportal/alum_login')
stud_login_url = reverse_lazy('jobportal/stud_login')


@login_required(login_url=alum_login_url)
def add_research_proposal(request):
    """
    Create new ResearchProposal instance.
    :param request:HttpRequest instance
    :return: HttpResponse instance
    """
    # get current user alumni
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    # if post request
    if request.method == "POST":
        # parse form data
        proposal_add_form = AddProposal(request.POST)
        # if form fields is valid
        if proposal_add_form.is_valid():
            # create new ResearchProposal instance
            proposal_instance = ResearchProposal(
                alum_owner=alum_instance,
                title=proposal_add_form.cleaned_data['title'],
                description=proposal_add_form.cleaned_data['description'],
                prerequsites=proposal_add_form.cleaned_data['prerequsites'],
                outcome=proposal_add_form.cleaned_data['outcome'],
                hours_week=proposal_add_form.cleaned_data['hours_week'],
                duration=proposal_add_form.cleaned_data['duration'],
                alum_current_address=proposal_add_form.cleaned_data['alum_current_address'],
                alum_current_institute=proposal_add_form.cleaned_data['alum_current_institute'],
                added=datetime.now(),
                last_updated=datetime.now()
            )
            # save instance
            proposal_instance.save()
            return redirect("mentormentee:alum_proposals")
        else:
            args = dict(proposal_add_form=proposal_add_form)
            return render(request, 'mentormentee/Alumni/add_proposal.html', args)
    else:
        args = dict(proposal_add_form=AddProposal())
        return render(request, 'mentormentee/Alumni/add_proposal.html', args)


@login_required(login_url=alum_login_url)
def applicants(request, proposalid):
    """
    Fetch applicants for ResearchProposal instance
    :param request: HttpRequest instance
    :param proposalid: id of ResearchProposal instance
    :return: HttpResponse instance
    """
    proposal_instance = get_object_or_404(ResearchProposal, id=proposalid)
    args = dict(relations_list=StudentProposalRelation.objects.all().filter(proposal=proposal_instance))
    return render(request, 'mentormentee/Alumni/applicants.html', args)


@login_required(login_url=stud_login_url)
def stud_proposals(request):
    """
    Fetch all proposals available for Student
    :param request:HttpRequest instance
    :return:HttpResponse instance
    """
    proposal_list = ResearchProposal.objects.all()
    args = {'proposal_list': proposal_list}
    return render(request, 'mentormentee/Student/proposals.html', args)


@login_required(login_url=stud_login_url)
def stud_review_proposal(request, proposalid):
    """
    Fetch details of a ResearchProposal instance for Student
    :param request: HttpRequest instance
    :param proposalid: id of ResearchProposal instance
    :return: HttpResponse instance
    """
    # ResearchProposal instance
    proposal_instance = get_object_or_404(ResearchProposal, id=proposalid)
    # Student instance
    stud_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    try:
        relation_instance = StudentProposalRelation.objects.get(stud=stud_instance, proposal=proposal_instance)
        opt_out_deadline = relation_instance.date_applied + timedelta(days=15)
    except StudentProposalRelation.DoesNotExist:
        relation_instance = None
        opt_out_deadline = ""
    args = dict(relation_instance=relation_instance, proposal_instance=proposal_instance,
                opt_out_deadline=opt_out_deadline)
    return render(request, 'mentormentee/Student/review_proposal.html', args)


@login_required(login_url=alum_login_url)
def alum_review_proposal(request, proposalid):
    """
    Fetch details of a ResearchProposal instance for Alumnus posted by Alumnus himself
    :param request: HttpRequest instance
    :param proposalid: id of ResearchProposal instance
    :return:HttpResponse instance
    """
    proposal_instance = get_object_or_404(ResearchProposal, id=proposalid)
    args = dict(proposal_instance=proposal_instance, delete_date=proposal_instance.added + timedelta(days=15))
    return render(request, 'mentormentee/Alumni/review_proposal.html', args)


@login_required(login_url=alum_login_url)
def review_applicant(request, proposalid, studid):
    """
    Fetch Student's response to a ResearchProposal instance
    :param request: HttpRequest instance
    :param proposalid: id of ResearchProposal instance
    :param studid:id of Student instance
    :return: HttpResponse instance
    """
    # Student instance
    stud_instance = get_object_or_404(Student, id=studid)
    # ResearchProposal instance
    proposal_instance = get_object_or_404(ResearchProposal, id=proposalid)
    # StudentProposalRelation instance
    relation_instance = get_object_or_404(StudentProposalRelation, proposal=proposal_instance, stud=stud_instance)
    args = dict(relation_instance=relation_instance)
    return render(request, 'mentormentee/Alumni/review_applicant.html', args)


@login_required(login_url=alum_login_url)
def alum_proposals(request):
    """
    Fetch all ResearchProposal instances for Alumnus posted by that Alumnus himself
    :param request: HttpRequest instance
    :return: HttpResponse instance
    """
    # Alumni instance
    alum_instance = get_object_or_404(Alumni, id=request.session['alum_instance_id'])
    # ResearchProposal instance
    proposal_list = ResearchProposal.objects.all().filter(alum_owner=alum_instance)
    args = dict(proposal_list=proposal_list)
    return render(request, 'mentormentee/Alumni/proposals.html', args)


@login_required(login_url=alum_login_url)
def edit_proposal(request, proposalid):
    """
    Edit a ResearchProposal instance.
    :param request: HttpRequest instance
    :param proposalid: id of ResearchProposal instance
    :return: HttpResponse instance
    """
    # ResearchProposal instance
    proposal_instance = get_object_or_404(ResearchProposal, id=proposalid)
    if request.method == "POST":
        # parse form data
        proposal_edit_form = EditProposal(request.POST)
        # if form is valid
        if proposal_edit_form.is_valid():
            # update ResearchProposal instance fields
            proposal_instance.last_updated = datetime.now()
            proposal_instance.alum_current_address = proposal_edit_form.cleaned_data['alum_current_address']
            proposal_instance.description = proposal_edit_form.cleaned_data['description']
            proposal_instance.hours_week = proposal_edit_form.cleaned_data['hours_week']
            proposal_instance.prerequsites = proposal_edit_form.cleaned_data['prerequsites']
            proposal_instance.outcome = proposal_edit_form.cleaned_data['outcome']
            proposal_instance.duration = proposal_edit_form.cleaned_data['duration']
            # Save ResearchProposal instance
            proposal_instance.save()
            return redirect("mentormentee:alum_proposals")
        else:
            args = dict(proposal_edit_form=proposal_edit_form, proposalid=proposalid)
            return render(request, 'mentormentee/Alumni/edit_proposal.html', args)
    else:
        # pre populate form
        proposal_edit_form = EditProposal(initial={
            'alum_current_address': proposal_instance.alum_current_address,
            'alum_current_institute': proposal_instance.alum_current_institute,
            'description': proposal_instance.description,
            'hours_week': proposal_instance.hours_week,
            'prerequsites': proposal_instance.prerequsites,
            'outcome': proposal_instance.outcome,
            'duration': proposal_instance.duration,
            'title': proposal_instance.title
        })
        args = dict(proposal_edit_form=proposal_edit_form, proposalid=proposalid)
        return render(request, 'mentormentee/Alumni/edit_proposal.html', args)


@login_required(login_url=alum_login_url)
def delete_proposal(request, proposalid):
    """
    Delete ResearchProposal instance.
    :param request: HttpRequest instance
    :param proposalid: id of ResearchProposal instance
    :return: HttpResponse instance
    """
    proposal_instance = get_object_or_404(ResearchProposal, id=proposalid)
    proposal_instance.delete()
    return redirect("mentormentee:alum_proposals")


@login_required(login_url=stud_login_url)
def stud_apply(request, proposalid):
    """
    Completes Student application for ResearchProposal complete
    by creating StudentProposalRelation instance.
    :param request: HttpRequest instance
    :param proposalid: ResearchProposal instance
    :return: HttpResponse instance
    """
    # fetch ResearchProposal instance
    proposal_instance = get_object_or_404(ResearchProposal, id=proposalid)
    if request.method == "POST":
        # parse form
        apply_form = StudApply(request.POST)
        # if form is valid
        if apply_form.is_valid():
            StudentProposalRelation.objects.create(
                proposal=proposal_instance,
                stud=get_object_or_404(Student, id=request.session['student_instance_id']),
                writeup=apply_form.cleaned_data['writeup'],
                max_hours=apply_form.cleaned_data['max_hours'],
                date_applied=datetime.now()
            )
            return redirect("mentormentee:stud_review_proposal", proposalid=proposal_instance.id)
        else:
            args = dict(apply_form=apply_form, proposal_instance=proposal_instance)
            return render(request, 'mentormentee/Student/apply.html', args)
    else:
        args = dict(apply_form=StudApply(), proposal_instance=proposal_instance)
        return render(request, 'mentormentee/Student/apply.html', args)


@login_required(login_url=alum_login_url)
def report_stud(request, relationid):
    """
    Report Student by updating report_byAlum* fields of StudentProposalRelation
    :param request: HttpRequest instance
    :param relationid: ResearchProposal instance
    :return: HttpResponse instance
    """
    # fetch ResearchProposal instance
    relation_instance = get_object_or_404(StudentProposalRelation, id=relationid)
    if request.method == "POST":
        # parse form
        report_form = ReportForm(request.POST)
        # if form is valid
        if report_form.is_valid():
            relation_instance.report_byAlum = True
            relation_instance.report_byAlum_reasons = report_form.cleaned_data['reasons']
            relation_instance.report_byAlum_date = datetime.now()
            relation_instance.save()
            return redirect("mentormentee:review_applicant", proposalid=relation_instance.proposal.id)
        else:
            args = dict(report_form=report_form, relation_instance=relation_instance)
            return render(request, "mentormentee/Alumni/report_stud.html", args)
    else:
        args = dict(report_form=ReportForm(), relation_instance=relation_instance)
        return render(request, "mentormentee/Alumni/report_stud.html", args)


@login_required(login_url=stud_login_url)
def opt_out(request, relationid):
    relation_instance = get_object_or_404(StudentProposalRelation, id=relationid)
    relation_instance.opt_out = True
    relation_instance.opt_out_date = datetime.now()
    relation_instance.save()
    return redirect("mentormentee:stud_review_proposal", proposalid=relation_instance.proposal.id)


@login_required(login_url=alum_login_url)
def report_alum(request,relationid):
    """
    Report alumni by editing 
    :param request: HttpRequest instance
    :param relationid: id of StudentProposalRelation instance
    :return: HttpResponse instance
    """
    relation_instance = get_object_or_404(StudentProposalRelation, id=relationid)
    if request.method == "POST":
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            relation_instance.report_byStud = True
            relation_instance.report_byStud_reasons = report_form.cleaned_data['reasons']
            relation_instance.report_byStud_date = datetime.now()
            relation_instance.save()
            return redirect('mentormentee:stud_review_proposal', proposalid=relation_instance.proposal.id,
                            studid=relation_instance.stud.id)
        else:
            args = {'report_form': report_form, 'relation_instance': relation_instance}
            return render('request', 'mentormentee/Student/report_alum.html', args)
    else:
        args = {'report_form': ReportForm(), 'relation_instance': relation_instance}
        return render(request, 'mentormentee/Student/report_alum.html', args)
