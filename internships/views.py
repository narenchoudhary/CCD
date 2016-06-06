from django.shortcuts import render
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from jobportal.models import Company, Student
from .models import IndInternship, ProgrammeInternRelation, StudentInternRelation
from .forms import RecruiterAddInternShip, AdminEditInternShip, InternProgFormSet
from jobportal.forms import SelectCVForm
from django.db import transaction

ALUM_LOGIN_URL = reverse_lazy('jobportal/alum_login')
STUD_LOGIN_URL = reverse_lazy('jobportal/stud_login')


def get_questions(studid):
    stud_instance = get_object_or_404(Student, id=studid)
    questions = []
    if bool(stud_instance.cv1):
        questions.append("cv1")
    if bool(stud_instance.cv2):
        questions.append("cv2")
    return questions


def company_all_interns(request):
    company_instance = Company.objects.get(id=request.session['company_instance_id'])
    intern_list = IndInternship.objects.filter(company_owner=company_instance)
    return render(request, 'internships/Company/all_interns.html', dict(intern_list=intern_list))


def company_add_intern(request):
    company_instance = Company.objects.get(id=request.session['company_instance_id'])
    add_form = RecruiterAddInternShip(request.POST or None)
    if request.method == 'POST':
        if add_form.is_valid():
            with transaction.atomic():
                intern_instance = add_form.save(commit=False)
                intern_instance.company_owner = company_instance
                intern_instance.posted_on = datetime.now()
                intern_instance.last_updated = timezone.now()
                intern_instance.opening_date = timezone.now() + timedelta(days=30)
                intern_instance.closing_date = timezone.datetime.now() + timedelta(days=50)
                intern_instance.save()
                intern_prog_rel = ProgrammeInternRelation(intern=intern_instance)
                intern_prog_rel.save()
            return redirect('internships:rec_all_interns')
        else:
            return render(request, 'internships/Company/add_intern.html', dict(form=add_form))
    else:
        return render(request, 'internships/Company/add_intern.html', dict(form=add_form))


def company_intern_details(request, internid):
    intern_instance = get_object_or_404(IndInternship, id=internid)
    prog_list = ProgrammeInternRelation.objects.filter(intern=intern_instance)
    prog_empty = True if (len(prog_list) == 1 and prog_list[0].year is None) else False
    args = dict(intern=intern_instance, prog_list=prog_list, prog_empty=prog_empty)
    return render(request, 'internships/Company/intern_details.html', args)


def company_edit_intern(request, internid):
    intern_instance = get_object_or_404(IndInternship, id=internid)
    edit_form = RecruiterAddInternShip(request.POST or None, instance=intern_instance)
    if request.method == 'POST':
        if edit_form.is_valid():
            edit_form.save()
            return redirect('internships:rec_intern_details', internid=intern_instance.id)
        else:
            args = dict(form=edit_form, intern=intern_instance)
            return render(request, 'internships/Company/edit_intern.html', args)
    else:
        args = dict(form=edit_form, intern=intern_instance)
        return render(request, 'internships/Company/edit_intern.html', args)


def company_add_progs(request, internid):
    intern_instance = get_object_or_404(IndInternship, id=internid)
    formset = InternProgFormSet(request.POST or None, instance=intern_instance)
    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect('internships:rec_intern_details', internid=intern_instance.id)
        else:
            return render(request, 'internships/Company/add_progs.html', dict(formset=formset, internid=internid))
    else:
        return render(request, 'internships/Company/add_progs.html', dict(formset=formset, internid=internid))


def company_intern_candidates(request, internid):
    intern_instance = get_object_or_404(IndInternship, id=internid)
    stud_rel_list = StudentInternRelation.objects.filter(intern=intern_instance)
    args = dict(stud_rel_list=stud_rel_list, intern=intern_instance, hide_action=False)
    return render(request, 'internships/Company/intern_candidates.html', args)


def company_intern_rel(request, relid):
    rel_instance = get_object_or_404(StudentInternRelation, id=relid)
    args = dict(rel=rel_instance)
    return render(request, 'internships/Company/intern_actions.html', args)


def company_intern_drop(request, internid):
    # TODO: Check no shortlist bug
    intern_instance = get_object_or_404(IndInternship, id=internid)
    stud_rels = list(StudentInternRelation.objects.filter(intern=intern_instance, dropped=False))
    approval_pending = False
    for rel in stud_rels:
        if rel.shortlist_init is True and rel.shortlist_approved is None:
            approval_pending = True
            break
        if rel.intern_init is True and rel.intern_approved is None:
            approval_pending = True
            break
        if rel.ppo_init is True and rel.intern_approved is None:
            approval_pending = True
            break
    if not approval_pending:
        for rel in stud_rels:
            rel.round += 1
            if rel.shortlist_init is False:
                rel.dropped = True
            if rel.shortlist_init is True and rel.intern_init is False:
                rel.shortlist_init = False
            rel.save()
    else:
        message = "Some approvals are not yet cleared by administrator. " \
                  "Round cannot be completed at this moment."
        messages.add_message(request, messages.WARNING, message)
    return redirect('internships:rec_intern_candidates', internid=internid)


def company_intern_shortlist(request, relid):
    rel_instance = get_object_or_404(StudentInternRelation, id=relid)
    if not rel_instance.dropped:
        if rel_instance.shortlist_init is False:
            rel_instance.shortlist_init = True
            rel_instance.save()
    return redirect('internships:rec_intern_rel', relid=rel_instance.id)


def company_intern_intern(request, relid):
    rel_instance = get_object_or_404(StudentInternRelation, id=relid)
    if not rel_instance.dropped:
        if rel_instance.shortlist_init is True and rel_instance.shortlist_approved is True:
            if rel_instance.intern_init is False and rel_instance.intern_approved is not True:
                rel_instance.intern_init = True
                rel_instance.save()
    return redirect('internships:rec_intern_rel', relid=rel_instance.id)


def company_intern_ppo(request, relid):
    rel_instance = get_object_or_404(StudentInternRelation, id=relid)
    if not rel_instance.dropped:
        if rel_instance.shortlist_init is True and rel_instance.shortlist_approved is True:
            if rel_instance.intern_init is True and rel_instance.intern_approved is True:
                if rel_instance.ppo_init is False and rel_instance.ppo_approved is None:
                    rel_instance.ppo_init = True
                    rel_instance.save()
    return redirect('internships:rec_intern_rel', relid=rel_instance.id)


def admin_all_interns(request):
    intern_list = IndInternship.objects.all()
    return render(request, 'internships/Admin/all_interns.html', dict(intern_list=intern_list))


def admin_intern_details(request, internid):
    intern_instance = get_object_or_404(IndInternship, id=internid)
    progs_list = ProgrammeInternRelation.objects.filter(intern=intern_instance)
    prog_empty = True if (len(progs_list) == 1 and progs_list[0].year is None) else False
    args = dict(intern=intern_instance, progs_list=progs_list, prog_empty=prog_empty)
    return render(request, 'internships/Admin/intern_details.html', args)


def admin_edit_intern(request, internid):
    intern_instance = get_object_or_404(IndInternship, id=internid)
    edit_form = AdminEditInternShip(request.POST or None, instance=intern_instance)
    if request.method == 'POST':
        if edit_form.is_valid():
            edit_form.save()
            return redirect('internships:admin_intern_details', internid=internid)
        else:
            args = dict(form=edit_form, internid=intern_instance.id)
            return render(request, 'internships/Admin/edit_intern.html', args)
    else:
        args = dict(form=edit_form, internid=intern_instance.id)
        return render(request, 'internships/Admin/edit_intern.html', args)


def admin_delete_intern(request, internid):
    intern_instance = get_object_or_404(IndInternship, id=internid)
    intern_instance.delete()
    return redirect('internships:admin_all_interns')


def admin_add_progs(request, internid):
    intern_instance = get_object_or_404(IndInternship, id=internid)
    formset = InternProgFormSet(request.POST or None, instance=intern_instance)
    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect('internships:admin_intern_details', internid=internid)
        else:
            args = dict(formset=formset, internid=internid)
            return render(request, 'internships/Admin/add_progs.html', args)
    else:
        args = dict(formset=formset, internid=internid)
        return render(request, 'internships/Admin/add_progs.html', args)


def admin_intern_candidates(request, internid):
    intern_instance = get_object_or_404(IndInternship, id=internid)
    rel_stud_list = StudentInternRelation.objects.filter(intern=intern_instance)
    args = dict(rel_stud_list=rel_stud_list, intern=intern_instance)
    return render(request, 'internships/Admin/intern_candidates.html', args)


def admin_rel_approvals(request, relid):
    # rel_instance = StudentInternRelation.objects.get(id=relid)
    rel_instance = get_object_or_404(StudentInternRelation, id=relid)
    return render(request, 'internships/Admin/intern_approvals.html', dict(rel=rel_instance))


def admin_approve_shortlist(request, relid):
    rel_instance = get_object_or_404(StudentInternRelation, id=relid)
    if not rel_instance.dropped:
        if rel_instance.shortlist_init is True and rel_instance.shortlist_approved is not True:
            rel_instance.shortlist_approved = True
            rel_instance.save()
    return redirect('internships:admin_intern_rel', relid=relid)


def admin_reject_shortlist(request, relid):
    rel_instance = get_object_or_404(StudentInternRelation, id=relid)
    if not rel_instance.dropped:
        if rel_instance.shortlist_init is True and rel_instance.shortlist_approved is None:
            rel_instance.shortlist_approved = False
            rel_instance.save()
    return redirect('internships:admin_intern_rel', relid=relid)


def admin_approve_intern(request, relid):
    rel_instance = get_object_or_404(StudentInternRelation, id=relid)
    if not rel_instance.dropped:
        if rel_instance.shortlist_init is True and rel_instance.shortlist_approved is True:
            if rel_instance.intern_init is True and rel_instance.intern_approved is None:
                rel_instance.intern_approved = True
                rel_instance.save()
    return redirect('internships:admin_intern_rel', relid=relid)


def admin_reject_intern(request, relid):
    rel_instance = get_object_or_404(StudentInternRelation, id=relid)
    if not rel_instance.dropped:
        if rel_instance.shortlist_init is True and rel_instance.shortlist_approved is True:
            if rel_instance.intern_init is True and rel_instance.intern_approved is None:
                rel_instance.intern_approved = False
                rel_instance.save()
    return redirect('internships:admin_intern_rel', relid=relid)


def admin_approve_ppo(request, relid):
    rel_instance = get_object_or_404(StudentInternRelation, id=relid)
    if not rel_instance.dropped:
        if rel_instance.shortlist_init is True and rel_instance.shortlist_approved is True:
            if rel_instance.intern_init is True and rel_instance.intern_approved is True:
                if rel_instance.ppo_init is True and rel_instance.ppo_approved is None:
                    rel_instance.ppo_approved = True
                    rel_instance.save()
    return redirect('internships:admin_intern_rel', relid=relid)


def admin_reject_ppo(request, relid):
    rel_instance = get_object_or_404(StudentInternRelation, id=relid)
    if not rel_instance.dropped:
        if rel_instance.shortlist_init is True and rel_instance.shortlist_approved is True:
            if rel_instance.intern_init is True and rel_instance.intern_approved is True:
                if rel_instance.ppo_init is True and rel_instance.ppo_approved is None:
                    rel_instance.ppo_approved = False
                    rel_instance.save()
    return redirect('internships:admin_intern_rel', relid=relid)


def stud_all_interns(request):
    stud_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    stud_prog = stud_instance.prog
    intern_list = set([e.intern for e in ProgrammeInternRelation.objects.filter(prog=stud_prog)])
    args = dict(intern_list=intern_list)
    return render(request, 'internships/Students/all_interns.html', args)


def stud_intern_details(request, internid):
    stud_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    intern_instance = get_object_or_404(IndInternship, id=internid)

    timezone_aware = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
    deadline_gone = True if intern_instance.closing_date < timezone_aware else False

    nocv = True if not bool(stud_instance.cv1) and not bool(stud_instance.cv2) else False
    try:
        stud_rel = StudentInternRelation.objects.get(stud=stud_instance, intern=intern_instance)
    except StudentInternRelation.DoesNotExist:
        stud_rel = None
    args = dict(intern=intern_instance, stud_rel=stud_rel, deadline_gone=deadline_gone, nocv=nocv)
    return render(request, 'internships/Students/intern_details.html', args)


def stud_intern_apply(request, internid):
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    intern_instance = get_object_or_404(IndInternship, id=internid)
    form = SelectCVForm(request.POST or None, extra=get_questions(student_instance.id))
    if request.method == 'POST':
        if form.is_valid():
            rel_instance = StudentInternRelation(
                stud=student_instance,
                intern=intern_instance
            )
            rel_instance.save()
            for (question, answer) in form.extra_answers():
                setattr(rel_instance, question, answer)
            rel_instance.save()
            return redirect('internships:stud_intern_details', internid=internid)
        else:
            args = dict(form=form, internid=internid)
            return render(request, 'internships/Students/intern_apply.html', args)
    else:
        args = dict(form=form, internid=internid)
        return render(request, 'internships/Students/intern_apply.html', args)


def stud_intern_applied_for(request):
    student_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    stud_intern_rel_list = StudentInternRelation.objects.get(stud=student_instance)
    args = dict(stud_intern_rel_list=stud_intern_rel_list)
    return render(request, 'internships/Students/interns_applied.html', args)


def stud_intern_deapply(request, internid):
    stud_instance = get_object_or_404(Student, id=request.session['student_instance_id'])
    intern_instance = get_object_or_404(IndInternship, id=internid)
    rel_instance = StudentInternRelation.objects.get(stud=stud_instance, intern=intern_instance)
    rel_instance.delete()
    return redirect('internships:stud_intern_details', internid=intern_instance.id)
