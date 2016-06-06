from django.conf.urls import url
from django.views.generic import TemplateView

from . import views, views_admin, views_company, views_alumni, views_print

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='jobportal/index.html'), name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),


    url(r'^stud/home/$', views.HomeView.as_view(), name='stud-home'),
    url(r'^stud/profile/update/$', views.ProfileUpdate.as_view(), name='stud-profile-update'),

    url(r'^stud/job/list/$', views.JobList.as_view(), name='stud-job-list'),
    url(r'^stud/job/(?P<jobid>\d+)/apply$', views.stud_applyjob, name='applyforjob'),
    url(r'^stud/job/(?P<jobid>\d+)/deapply$', views.stud_deapplyjob, name='deapplyforjob'),
    url(r'^stud/jobrel/list/$', views.JobList.as_view(), name='stud-jobrel-list'),
    url(r'^stud/job/(?P<pk>\d+)/detail/$', views.JobDetail.as_view(), name='stud-job-detail'),

    url(r'^stud/cv/$', views.CVDetail.as_view(), name='stud-cv-detail'),
    url(r'^stud/cv/create/$', views.CVCreate.as_view(), name='stud-cv-create'),
    url(r'^stud/cv/update/$', views.CVUpdate.as_view(), name='stud-cv-update'),

    url(r'^stud/event/list/$', views.EventList.as_view(), name='stud-event-list'),
    url(r'^stud/event/<?pk>/detail$', views.EventDetail.as_view(), name='stud-event-detail'),

    url(r'^stud/avatar/detail/$', views.AvatarDetail.as_view(), name='stud-avatar-detail'),
    url(r'^stud/avatar/create/$', views.AvatarCreate.as_view(), name='stud-avatar-create'),
    url(r'^stud/avatar/update/$', views.AvatarUpdate.as_view(), name='stud-avatar-update'),

    url(r'^stud/sign/detail/$', views.SignatureDetail.as_view(), name='stud-sign-detail'),
    url(r'^stud/sign/create/$', views.SignatureCreate.as_view(), name='stud-sign-create'),
    url(r'^stud/sign/update/$', views.SignatureUpdate.as_view(), name='stud-sign-update'),


    url(r'^alum_home/$', views_alumni.alum_home, name='alum_home'),
    url(r'^alum_view_profile$', views_alumni.view_profile, name='alum_view_profile'),
    url(r'^alum_edit_profile$', views_alumni.edit_profile, name='alum_edit_profile'),
    url(r'^alum_cv_upload$', views_alumni.upload_cv, name='alum_cv_upload'),


    url(r'^company/signup/$', views_company.CompanySignUpView.as_view(), name='company-signup'),
    url(r'^company/signupconfirm/$', TemplateView.as_view(template_name='jobportal/Company/signupconfirm.html'),
        name='signup-confirm'),
    url(r'^company/home/$', views_company.HomeView.as_view(), name='company-home'),

    url(r'^company/password/update/$', views_company.PasswordChangeView.as_view(), name='company-password-update'),
    url(r'^company/profile/detail/$', views_company.ProfileDetail.as_view(), name='company-profile-detail'),
    url(r'^company/profile/update/$', views_company.ProfileUpdate.as_view(), name='company-profile-update'),

    url(r'^companydropjob/(?P<jobid>\d+)$', views_company.job_drop, name='companydropjob'),

    url(r'^company/job/list/$', views_company.JobList.as_view(), name='company-job-list'),
    url(r'^company/job/create/$', views_company.JobCreate.as_view(), name='company-job-create'),
    url(r'^company/job/(?P<pk>\d+)/detail/$', views_company.JobDetail.as_view(), name='company-job-detail'),
    url(r'^company/job/(?P<pk>\d+)/update/$', views_company.JobUpdate.as_view(), name='company-job-update'),
    url(r'^company/job/(?P<pk>\d+)/delete/$', views_company.JobDelete.as_view(), name='company-job-delete'),

    url(r'^company/job/(?P<jobid>\d+)/prog/update/$', views_company.add_progs, name='company_add_progs'),

    url(r'^company/event/list/$', views_company.company_eventsandstatus, name='companyeventsandstatus'),
    url(r'^company/(?P<pk>\d+)/jobrel/list/$', views_company.JobRelList.as_view(), name='company-jobrel-list'),

    # Job Actions : Students
    url(r'^jobaction/(?P<jobid>(\d+))/(?P<studid>(\d+))/$', views_company.job_stud_relation, name="jobaction"),
    url(r'^company/jobrel/stud/(?P<relationid>\d+)/shortlist/$', views_company.job_shortlist, name='shortlist'),
    url(r'^company.//jobrel/stud/(?P<relationid>\d+)/unshortlist/$', views_company.job_unshortlist, name='unshortlist'),
    url(r'^job_place/(?P<relationid>\d+)$', views_company.job_place, name='place'),
    url(r'^job_unplace/(?P<relationid>\d+)$', views_company.job_unplace, name='unplace'),
    # Job Actions: Alumni
    url(r'^jobaction2/(?P<jobid>(\d+))/(?P<alumid>(\d+))/$', views_company.job_alum_relation, name="jobaction2"),
    url(r'^job_shortlist2/(?P<relationid>\d+)/$', views_company.job_shortlist2, name="shortlist2"),
    url(r'^job_unshortlist2/(?P<relationid>\d+)/$', views_company.job_unshortlist2, name="unshortlist2"),
    url(r'^job_place2/(?P<relationid>\d+)/$', views_company.job_place2, name="place2"),
    url(r'^job_unplace2/(?P<relationid>\d+)/$', views_company.job_unplace2, name="unplace2"),
    # File Downloads
    url(r'^download_cvs/(?P<jobid>\d+)$', views_company.download_cvs, name="download_cvs"),
    # Calendar: Do it later
    url(r'^company/event/create/$', views_print.company_requestevent, name='companyrequestevent'),



    url(r'^admin/home/$', views_admin.HomeView.as_view(), name="admin-home"),

    url(r'^admin/job/(?P<jobid>\d+)/approve/$', views_admin.approve_job, name='approve_job'),
    url(r'^admin_approval/(?P<object_type>[A-Za-z_]+)$', views_admin.admin_approvals, name='admin_approval'),
    # Search Users
    url(r'^admin/manage/$', views_admin.admin_manage, name="admin_manage"),
    url(r'^admin/search/students/$', views_admin.search_students, name='search_students'),
    url(r'^admin/student/create/$', views_admin.add_student, name='add_student'),

    url(r'^review_stud_profile/(?P<studid>\d+)$', views_admin.review_stud_profile, name='review_stud_profile'),
    url(r'^edit_student/(?P<studid>\d+)$', views_admin.edit_student, name='edit_student'),

    url(r'^admin/company/signup/list/$', views_admin.CompanySignupList.as_view(), name='admin-company-signup-list'),


    url(r'^admin/company/list/$', views_admin.CompanyList.as_view(), name='admin-company-list'),
    url(r'^admin/company/create/$', views_admin.CompanyCreate.as_view(), name='admin-company-create'),
    url(r'^admin/company/(?P<pk>\d+)/detail/$', views_admin.CompanyDetail.as_view(), name='admin-company-detail'),
    url(r'^admin/company/(?P<pk>\d+)/update/$', views_admin.CompanyUpdate.as_view(), name='admin-company-update'),
    url(r'^admin/company/(?P<pk>\d+)/delete/$', views_admin.CompanyDelete.as_view(), name='admin-company-delete'),
    url(r'^admin/company/(?P<pk>\d+)/approve/$', views_admin.CompanyApproveView.as_view(), name='admin-company-approve'),

    url(r'^admin/job/list/$', views_admin.JobList.as_view(), name='admin-job-list'),
    url(r'^admin/job/(?P<pk>\d+)/detail/$', views_admin.JobDetail.as_view(), name='admin-job-detail'),
    url(r'^admin/job/(?P<pk>\d+)/update/$', views_admin.JobUpdate.as_view(), name='admin-job-update'),
    url(r'^admin/job/(?P<pk>\d+)/approve/$', views_admin.JobUpdate.as_view(), name='admin-job-approve'),

    url(r'^admin/job/(?P<jobid>\d+)/prog/list/update$', views_admin.edit_progs, name='admin-job-progs-update'),
    url(r'^admin/job/(?P<jobid>\d+)/candidate/list/$', views_admin.job_candidates, name='job_candidates'),
    url(r'^approve_action/(?P<applicant_type>[A-za-z]+)/(?P<relationid>\d+)$', views_admin.approve_action,
        name='approve_action'),
    url(r'^admin/jobrel/stud/(?P<relationid>\d+)/approve/$', views_admin.approve_stud_relation, name='approve_stud'),

    url(r'^admin/department/list/$', views_admin.DepartmentList.as_view(), name="department-list"),
    url(r'^admin/department/create/$', views_admin.DepartmentCreate.as_view(), name="department-create"),
    url(r'^admin/department/(?P<pk>\d+)/detail/$', views_admin.DepartmentDetail.as_view(), name="department-detail"),
    url(r'^admin/department/(?P<pk>\d+)/update/$', views_admin.DepartmentUpdate.as_view(), name='department-update'),
    url(r'^admin/department/(?P<pk>\d+)/delete/$', views_admin.DepartmentDelete.as_view(), name='department-delete'),

    url(r'^admin/programme/list/$', views_admin.ProgrammeList.as_view(), name="programme-list"),
    url(r'^admin/programme/create/$', views_admin.ProgrammeCreate.as_view(), name="programme-create"),
    url(r'^admin/programme/(?P<pk>\d+)/update/$', views_admin.ProgrammeUpdate.as_view(), name='programme-update'),
    url(r'^admin/programme/(?P<pk>\d+)/delete/$', views_admin.ProgrammeDelete.as_view(), name='programme-delete'),

    url(r'^admin/year/list/$', views_admin.YearList.as_view(), name="year-list"),
    url(r'^admin/year/create/$', views_admin.YearCreate.as_view(), name="year-add"),
    url(r'^admin/years/(?P<pk>\d+)/delete/$', views_admin.YearDelete.as_view(), name='year-delete'),

    url(r'^pdfgen/$', views_print.stud_pdf, name='pdfgen'),
    url(r'^requestevent/$', views_print.requestevent, name='requestevent'),
    url(r'^eventsandstatus/$', views_print.eventsandstatus, name='eventsandstatus'),
    url(r'^printcsv/(?P<jobid>\d+)$', views_print.candidates_stud_csv, name='printcsv'),
    url(r'^companies_csv/$', views_print.companies_csv, name='companies_csv'),
]
