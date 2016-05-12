from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from .models import Admin, Student, Job, StudentJobRelation, Company, CompanyReg, Department, Year, \
    Programme, ProgrammeJobRelation, UserProfile
from .forms import AddCompany, AddEditDepartment, AddEditProgramme, AddEditYear, AdminJobEditForm, \
    AddStudent, JobProgFormSet, EditStudentAdmin, StudentSearchForm, EditCompany
from internships.models import IndInternship, StudentInternRelation

ADMIN_LOGIN_URL = reverse_lazy('login')


# Admin home
@login_required(login_url=ADMIN_LOGIN_URL)
def admin_home(request):
    admin_instance = get_object_or_404(Admin, id=request.session['admin_instance_id'])
    requestscount = CompanyReg.objects.all().count()
    companiescount = Company.objects.all().count()
    jobscount = Job.objects.all().count()
    args = dict(admin=admin_instance, requestscount=requestscount,
                companiescount=companiescount, jobscount=jobscount)
    return render(request, 'jobportal/Admin/home.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def admin_logout(request):
    auth.logout(request)
    return render(request, "jobportal/logout.html")


@login_required(login_url=ADMIN_LOGIN_URL)
def departments(request):
    args = dict(departments=Department.objects.all())
    return render(request, 'jobportal/Admin/departments.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def add_department(request):
    if request.method == 'POST':
        department_form = AddEditDepartment(request.POST)
        if department_form.is_valid():
            department_form.save()
            return redirect("departments")
        else:
            args = dict(department_add_form=department_form, add=True)
            return render(request, 'jobportal/Admin/add_edit_department.html', args)
    else:
        args = dict(department_add_form=AddEditDepartment(), add=True)
        return render(request, 'jobportal/Admin/add_edit_department.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def edit_department(request, deptid):
    if request.method == "POST":
        department_instance = Department.objects.get(id=deptid)
        department_form = AddEditDepartment(request.POST, instance=department_instance)
        if department_form.is_valid():
            department_form.save()
            return redirect('departments')
        else:
            args = dict(department_edit_form=department_form, edit=True, deptid=deptid)
            return render(request, 'jobportal/Admin/add_edit_department.html', args)
    else:
        department_instance = get_object_or_404(Department, id=deptid)
        args = dict(department_edit_form=AddEditDepartment(instance=department_instance), edit=True, deptid=deptid)
        return render(request, 'jobportal/Admin/add_edit_department.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def delete_department(deptid):
    dept_instance = get_object_or_404(Department, id=deptid)
    dept_instance.delete()
    return redirect("departments")


@login_required(login_url=ADMIN_LOGIN_URL)
def programmes(request):
    args = dict(programmes=Programme.objects.all())
    return render(request, 'jobportal/Admin/programmes.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def add_programme(request):
    if request.method == "POST":
        programme_form = AddEditProgramme(request.POST)
        if programme_form.is_valid():
            programme_form.save()
            return redirect('programmes')
        else:
            args = dict(add_programme_form=programme_form, add=True)
            return render(request, 'jobportal/Admin/add_edit_programmes.html', args)
    else:
        args = dict(add_programme_form=AddEditProgramme(), add=True)
        return render(request, 'jobportal/Admin/add_edit_programmes.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def edit_programme(request, progid):
    if request.method == "POST":
        prog_instance = Programme.objects.get(id=progid)
        programe_form = AddEditProgramme(request.POST, prog_instance)
        if programe_form.is_valid():
            programe_form.save()
            return redirect('programmes')
        else:
            args = dict(edit_programme_form=programe_form, edit=True, progid=progid)
            return render(request, 'jobportal/Admin/add_edit_programmes.html', args)
    else:
        prog_instance = Programme.objects.get(id=progid)
        edit_programme_form = AddEditProgramme(instance=prog_instance)
        args = dict(edit_programme_form=edit_programme_form, edit=True, progid=progid)
        return render(request, 'jobportal/Admin/add_edit_programmes.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def delete_programme(progid):
    prog_instance = get_object_or_404(Programme, id=progid)
    prog_instance.delete()
    return redirect("programmes")


@login_required(login_url=ADMIN_LOGIN_URL)
def years(request):
    all_years = Year.objects.all()
    args = dict(years=all_years)
    return render(request, 'jobportal/Admin/years.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def add_year(request):
    add_year_form = AddEditYear(request.POST or None)
    if request.method == "POST":
        if add_year_form.is_valid():
            add_year_form.save()
            return redirect('years')
        else:
            args = dict(add_year_form=add_year_form, add=True)
            return render(request, 'jobportal/Admin/add_edit_years.html', args)
    else:
        args = dict(add_year_form=add_year_form, add=True)
        return render(request, 'jobportal/Admin/add_edit_years.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def delete_year(yearid):
    year_instance = get_object_or_404(Year, id=yearid)
    year_instance.delete()
    return redirect("years")


@login_required(login_url=ADMIN_LOGIN_URL)
def jobs(request):
    alljobs = Job.objects.all()
    args = dict(jobs=alljobs)
    return render(request, "jobportal/Admin/jobs.html", args)


@login_required(login_url=ADMIN_LOGIN_URL)
def review_job(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    progs_list = ProgrammeJobRelation.objects.filter(job=job_instance)
    args = dict(job_instance=job_instance, progs_list=progs_list)
    return render(request, 'jobportal/Admin/review_job.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def edit_job(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    job_add_form = AdminJobEditForm(request.POST or None, instance=job_instance)
    if request.method == "POST":
        if job_add_form.is_valid():
            job_add_form.save()
            return redirect('review_job', jobid=jobid)
        else:
            args = dict(edit_job_form=job_add_form, job=job_instance)
            return render(request, 'jobportal/Admin/edit_job.html', args)
    else:
        args = dict(edit_job_form=job_add_form, job=job_instance)
        return render(request, 'jobportal/Admin/edit_job.html', args)


def edit_progs(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    formset = JobProgFormSet(request.POST or None, instance=job_instance)
    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect('review_job', jobid=job_instance.id)
        else:
            args = dict(formset=formset, job_instance=job_instance)
            return render(request, 'jobportal/Admin/edit_progs_formset.html', args)
    else:
        args = dict(formset=formset, job_instance=job_instance)
        return render(request, 'jobportal/Admin/edit_progs_formset.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def delete_job(jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    job_instance.delete()
    return redirect('jobs')


@login_required(login_url=ADMIN_LOGIN_URL)
def approve_job(jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    job_instance.approved = True
    job_instance.approved_on = datetime.now()
    job_instance.save()
    return redirect('review_job', jobid=job_instance.id)


@login_required(login_url=ADMIN_LOGIN_URL)
def sent_back_job(jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    job_instance.sent_back = True
    job_instance.save()
    return redirect('review_job', jobid=job_instance.id)


@login_required(login_url=ADMIN_LOGIN_URL)
def admin_manage(request):
    return render(request, 'jobportal/Admin/manage.html')


@login_required(login_url=ADMIN_LOGIN_URL)
def add_student(request):
    add_student_form = AddStudent(request.POST or None)
    if request.method == "POST":
        if add_student_form.is_valid():
            username = add_student_form.cleaned_data['username']
            password = add_student_form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user_profile_instance = UserProfile.objects.create(user=user, login_type="Current Student")
            student_instance = add_student_form.save(commit=False)
            student_instance.user = user_profile_instance
            student_instance.save()
            args = dict(created='Student', webmail=username)
            return render(request, 'jobportal/Admin/manage.html', args)
        else:
            args = dict(add_student_form=add_student_form)
            return render(request, 'jobportal/Admin/add_student.html', args)
    else:
        args = dict(add_student_form=add_student_form)
        return render(request, 'jobportal/Admin/add_student.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def search_students(request):
    studentsearch_form = StudentSearchForm(request.POST or None)
    if request.method == "POST":
        if studentsearch_form.is_valid():
            student_programme = studentsearch_form.cleaned_data['programme']
            student_year = studentsearch_form.cleaned_data['year']
            student_departent = studentsearch_form.cleaned_data['department']
            students_list = Student.objects.all().filter(
                prog__name=student_programme).filter(
                dept__dept_code=student_departent).filter(
                year__current_year=student_year)

            args = dict(students_list=students_list, student_search_form=studentsearch_form)
            return render(request, 'jobportal/Admin/all_users.html', args)
        else:
            args = dict(student_search_form=studentsearch_form)
            return render(request, 'jobportal/Admin/all_users.html', args)
    else:
        args = dict(student_search_form=studentsearch_form)
        return render(request, 'jobportal/Admin/all_users.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def review_stud_profile(request, studid):
    student_instance = get_object_or_404(Student, id=studid)
    args = dict(edited='Student', student_instance=student_instance)
    return render(request, 'jobportal/Admin/review_profile.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def edit_student(request, studid):
    student_instance = get_object_or_404(Student, id=studid)
    edit_student_form = EditStudentAdmin(request.POST or None, instance=student_instance)
    if request.method == "POST":
        if edit_student_form.is_valid():
            edit_student_form.save()
            return redirect('review_stud_profile', studid=studid)
        else:
            args = dict(student_profile_edit_form=edit_student_form, studid=studid)
            return render(request, 'jobportal/Admin/edit_student_profile.html', args)
    else:
        args = dict(student_profile_edit_form=edit_student_form, studid=studid)
        return render(request, 'jobportal/Admin/edit_student_profile.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def companies(request):
    comapnies = Company.objects.all()
    args = dict(companies=comapnies)
    return render(request, "jobportal/Admin/companies.html", args)


@login_required(login_url=ADMIN_LOGIN_URL)
def add_company(request):
    add_company_form = AddCompany(request.POST or None)
    if request.method == "POST":
        if add_company_form.is_valid():
            username = add_company_form.cleaned_data['username']
            password = add_company_form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user_profile_instance = UserProfile.objects.create(user=user, login_type="Company")
            company_instance = add_company_form.save()
            company_instance.user = user_profile_instance
            company_instance.save()
            return redirect("companies")
        else:
            add_company_form = add_company_form
            args = {'add_company_form': add_company_form, 'request': False}
            return render(request, 'jobportal/Admin/add_company.html', args)
    else:
        add_company_form = AddCompany()
        args = {'add_company_form': add_company_form, 'request': False}
        return render(request, 'jobportal/Admin/add_company.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def review_company_profile(request, companyid):
    company_instance = get_object_or_404(Company, id=companyid)
    job_list = Job.objects.all().filter(company_owner=company_instance)
    intern_list = IndInternship.objects.all().filter(company_owner=company_instance)
    args = dict(edited='Company', company_instance=company_instance,
                job_list=job_list, intern_list=intern_list)
    return render(request, 'jobportal/Admin/review_profile.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def delete_company(companyid):
    company_instance = get_object_or_404(Company, id=companyid)
    user_instance = User.objects.get(username=company_instance.user.user.username)
    user_instance.delete()
    return redirect('companies')


@login_required(login_url=ADMIN_LOGIN_URL)
def edit_company(request, companyid):
    company_instance = get_object_or_404(Company, id=companyid)
    edit_company_form = EditCompany(request.POST or None, instance=company_instance)
    if request.method == "POST":
        if edit_company_form.is_valid():
            edit_company_form.save()
            return redirect('review_company_profile', companyid=companyid)
        else:
            args = dict(company_profile_edit_form=edit_company_form, companyid=companyid)
            return render(request, 'jobportal/Admin/edit_company_profile.html', args)
    else:
        args = dict(company_profile_edit_form=edit_company_form, companyid=companyid)
        return render(request, 'jobportal/Admin/edit_company_profile.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def signup_requests(request):
    args = dict(requests=CompanyReg.objects.all())
    return render(request, 'jobportal/Admin/signup_requests.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def del_signup_request(companyregid):
    companyreg_instance = get_object_or_404(CompanyReg, id=companyregid)
    companyreg_instance.delete()
    return redirect("signup_requests")


@login_required(login_url=ADMIN_LOGIN_URL)
def review_request_profile(request, companyregid):
    companyreg_instance = CompanyReg.objects.get(id=companyregid)
    args = dict(edited='Request', request=companyreg_instance)
    return render(request, 'jobportal/Admin/review_profile.html', args)


# TODO: Can we merge CompanyReg with Company?
# TODO: Is it safe to do so?
@login_required(login_url=ADMIN_LOGIN_URL)
def add_company_by_signup_request(request, companyregid):
    add_company_form_data = AddCompany(request.POST or None)
    if request.method == "POST":
        if add_company_form_data.is_valid():
            username = add_company_form_data.cleaned_data['username']
            password = add_company_form_data.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user_profile_instance = UserProfile.objects.create(user=user, login_type="Company")
            company_instance = add_company_form_data.save(commit=False)
            company_instance.user = user_profile_instance
            company_instance.save()
            companyreg_instance = CompanyReg.objects.get(id=companyregid)
            companyreg_instance.delete()
            messages.add_message(request, messages.SUCCESS, "Company " + add_company_form_data.cleaned_data[
                'company_name'] + " has been successfully added.")
            return redirect("companies")
        else:
            add_company_form = add_company_form_data
            args = {'add_company_form': add_company_form, 'request': True, 'companyregid': companyregid}
            return render(request, 'jobportal/Admin/add_company.html', args)
    else:
        companyreg_instance = CompanyReg.objects.get(id=companyregid)
        add_company_form = AddCompany(initial={
            'company_name': companyreg_instance.company_name_reg,
            'description': companyreg_instance.description_reg,
            'website': companyreg_instance.website_reg,
            'organization_type': companyreg_instance.organization_type_reg,
            'industry_sector': companyreg_instance.industry_sector_reg,
            'head_hr_name': companyreg_instance.head_hr_name_reg,
            'head_hr_designation': companyreg_instance.head_hr_designation_reg,
            'head_hr_email': companyreg_instance.head_hr_email_reg,
            'head_hr_mobile': companyreg_instance.head_hr_mobile_reg,
            'head_hr_fax': companyreg_instance.head_hr_fax_reg,
            'first_hr_name': companyreg_instance.first_hr_name_reg,
            'first_hr_designation': companyreg_instance.first_hr_designation_reg,
            'first_hr_email': companyreg_instance.first_hr_email_reg,
            'first_hr_mobile': companyreg_instance.first_hr_mobile_reg,
            'first_hr_fax': companyreg_instance.first_hr_fax_reg
        })
        args = {'add_company_form': add_company_form, 'request': True, 'companyregid': companyregid}
        return render(request, 'jobportal/Admin/add_company.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def job_candidates(request, jobid):
    job_instance = get_object_or_404(Job, id=jobid)
    relation_list_stud = StudentJobRelation.objects.all().filter(job=job_instance)
    args = dict(relation_list_stud=relation_list_stud, job_instance=job_instance)
    return render(request, 'jobportal/Admin/job_candidates.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def approve_action(request, applicant_type, relationid):
    if applicant_type == "stud":
        relation_instance = get_object_or_404(StudentJobRelation, id=relationid)
    else:
        relation_instance = None
    args = dict(relation_instance=relation_instance, applicant_type=applicant_type)
    return render(request, 'jobportal/Admin/approve_actions.html', args)


@login_required(login_url=ADMIN_LOGIN_URL)
def approve_stud_relation(relationid):
    relation_instance = get_object_or_404(StudentJobRelation, id=relationid)

    if relation_instance.placed_init is True:
        if relation_instance.placed_approved is not True:
            relation_instance.placed_approved = True
            relation_instance.save()

    if relation_instance.shortlist_init is True:
        if relation_instance.shortlist_approved is not True:
            relation_instance.shortlist_approved = True
            relation_instance.save()
    return redirect("approve_action", applicant_type="stud", relationid=relationid)


@login_required(login_url=ADMIN_LOGIN_URL)
def admin_approvals(request, object_type):
    if str(object_type) == "job":
        job_list = Job.objects.all().filter(approved__isnull=True)
        intern_list = IndInternship.objects.all().filter(approved__isnull=True)
        args = dict(intern_list=intern_list, job_list=job_list)
        return render(request, 'jobportal/Admin/unapprv_job.html', args)
    elif str(object_type) == "job_progress":
        # job_shortlist = StudentJobRelation.objects.all().filter(
        #     shortlist_init=True, shortlist_approved__isnull=True
        # )
        # job_place_list = StudentJobRelation.objects.all().filter(
        #     placed_init=True, placed_approved__isnull=True
        # )
        intern_shortlist = StudentInternRelation.objects.all().filter(
            shortlist_init=True, shortlist_approved__isnull=True
        )
        intern_hire = StudentInternRelation.objects.all().filter(
            intern_init=True, intern_approved__isnull=True
        )
        intern_ppo = StudentInternRelation.objects.all().filter(
            ppo_init=True, ppo_approved__isnull=True
        )
        args = dict(intern_hire=intern_hire, intern_ppo=intern_ppo, intern_shortlist=intern_shortlist)
        return render(request, 'jobportal/Admin/unapprv_progress.html', args)
    else:
        return redirect("admin_home")
