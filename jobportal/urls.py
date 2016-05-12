from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from . import views_company
from . import views_admin
from . import views_alumni
from . import views_print

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='jobportal/index.html'), name='index'),
    url(r'^login$', views.login, name='login'),

    # ----------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    # Current Student Urls
    # student logout
    url(r'^stud_logout/$', views.stud_logout, name='stud_logout'),
    # student home
    url(r'^stud_home/$', views.stud_home, name='stud_home'),
    # student edit profile
    url(r'^editstudprofile/$', views.edit_stud_profile, name='editstudprofile'),
    # student view available jobs
    url(r'^studviewjobs/$', views.stud_viewjobs, name='studviewjobs'),
    # apply for job
    url(r'^applyforjob/(?P<jobid>\d+)$', views.stud_applyjob, name='applyforjob'),
    # remove application
    url(r'^deapplyforjob/(?P<jobid>\d+)$', views.stud_deapplyjob, name='deapplyforjob'),
    # jobs already applied for
    url(r'^stud_jobsappliedfor/$', views.stud_jobsappliedfor, name='stud_jobsappliedfor'),
    # job details
    url(r'^jobdetails/(?P<jobid>\d+)$', views.stud_jobdetails, name='jobdetails'),
    # CVs
    url(r'^viewcvs/$', views.view_cvs, name='viewcvs'),
    # upload CVs
    url(r'^cvupload/$', views.cv_upload, name='cvupload'),
    # delete CV
    url(r'^delcv/(?P<cvno>\d+)$', views.del_cv, name='deletecv'),
    # TODO: Yet to be done
    url(r'^viewevents/$', views.eventlist, name='viewevents'),
    # upload avatar and signature
    url(r'^viewavatar/$', views.view_avatar, name='viewavatar'),
    url(r'^avatarupload/$', views.upload_avatar_sign, name='avatarupload'),
    # ----------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------
    # Alumni Urls
    url(r'^alum_logout/$', views_alumni.alum_logout, name='alum_logout'),
    url(r'^alum_home/$', views_alumni.alum_home, name='alum_home'),
    url(r'^alum_view_profile$', views_alumni.view_profile, name='alum_view_profile'),
    url(r'^alum_edit_profile$', views_alumni.edit_profile, name='alum_edit_profile'),
    url(r'^alum_cv_upload$', views_alumni.upload_cv, name='alum_cv_upload'),
    # url(r'^view_jobs/$', views_alumni.view_jobs, name='alumviewjobs'),
    # url(r'^postalumjob/$', views_alumni.alum_add_job, name='postalumjob'),
    # url(r'^viewalumjob/$', views_alumni.view_jobs, name='viewalumjob'),
    # url(r'^editalumjob/(?P<jobid>\d+)$', views_alumni.alum_edit_job, name='editalumjob'),
    # url(r'^delalumjob/(?P<jobid>\d+)$', views_alumni.alum_del_job, name='delalumjob'),
    # url(r'^apply/(?P<jobid>\d+)$', views_alumni.alum_candidates, name='apply'),
    # # Availabe Jobs: Alumni
    # url(r'^availablejobs/$', views_alumni.jobs_availabe, name="availablejobs"),
    # url(r'^alum_jobdetails/(?P<jobid>\d+)$', views_alumni.alum_jobdetails, name="alum_jobdetails"),
    # url(r'^alum_apply/(?P<jobid>\d+)$', views_alumni.alum_apply, name="alum_applyforjob"),
    # url(r'^alum_deapply/(?P<jobid>\d+)$', views_alumni.alum_deapply, name="alum_deapplyforjob"),
    # url(r'^alum_jobsappliedfor/$', views_alumni.alum_jobsappliedfor, name='alum_jobsappliedfor'),
    # # Job Actions: Students
    # url(r'^alumnicandidates/(?P<jobid>\d+)$', views_alumni.alum_candidates, name='alumcandidates'),
    # url(r'^alum_jobaction/(?P<jobid>(\d+))/(?P<studid>(\d+))/$', views_alumni.job_stud_relation, name='alum_jobaction'),
    # url(r'^alum_job_shortlist/(?P<relationid>\d+)$', views_alumni.job_shortlist, name='alum_shortlist'),
    # url(r'^alum_job_unshortlist/(?P<relationid>\d+)$', views_alumni.job_unshortlist, name='alum_unshortlist'),
    # url(r'^alum_job_place/(?P<relationid>\d+)$', views_alumni.job_place, name='alum_place'),
    # url(r'^alum_job_unplace/(?P<relationid>\d+)$', views_alumni.job_unplace, name='alum_unplace'),
    # Job Actions: Alumni
    # url(r'^alum_jobaction2/(?P<jobid>(\d+))/(?P<alumid>(\d+))/$', views_alumni.job_alum_relation,
    #     name='alum_jobaction2'),
    # url(r'^alum_job_shortlist2/(?P<relationid>\d+)$', views_alumni.job_shortlist2, name='alum_shortlist2'),
    # url(r'^alum_job_unshortlist2/(?P<relationid>\d+)$', views_alumni.job_unshortlist2, name='alum_unshortlist2'),
    # url(r'^alum_job_place2/(?P<relationid>\d+)$', views_alumni.job_place2, name='alum_place2'),
    # url(r'^alum_job_unplace2/(?P<relationid>\d+)$', views_alumni.job_unplace2, name='alum_unplace2'),
    # ----------------------------------------------------------------------------------------
    # experiments
    url(r'^pdfgen/$', views.stud_pdf, name='pdfgen'),
    url(r'^requestevent/$', views.requestevent, name='requestevent'),
    url(r'^eventsandstatus/$', views.eventsandstatus, name='eventsandstatus'),
    # prints
    url(r'^printcsv/(?P<jobid>\d+)$', views_print.candidates_stud_csv, name='printcsv'),
    url(r'^companies_csv/$', views_print.companies_csv, name='companies_csv'),
    # ----------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------
    # Company
    url(r'^signup/$', views_company.signup, name='signup'),
    url(r'^signupconfirm/$', views_company.signup_confirm, name='signupconfirm'),
    url(r'^companylogout/$', views_company.company_logout, name='companylogout'),
    url(r'^companyhome/$', views_company.company_home, name='companyhome'),
    url(r'^companyprofile/$', views_company.company_profile, name='companyprofile'),
    url(r'^companyviewjobs/$', views_company.view_jobs, name='companyviewjobs'),
    url(r'^companyjob/(?P<jobid>\d+)$', views_company.view_job, name='companyjob'),
    url(r'^company_add_progs/(?P<jobid>\d+)$', views_company.add_progs, name='company_add_progs'),
    url(r'^companyaddjob/$', views_company.company_add_job, name='companyaddjob'),
    url(r'^companyeditjob/(?P<jobid>\d+)$', views_company.company_edit_job, name='companyeditjob'),
    url(r'^companydeljob/(?P<jobid>\d+)$', views_company.company_del_job, name='companydeljob'),
    url(r'^companydropjob/(?P<jobid>\d+)$', views_company.job_drop, name='companydropjob'),
    url(r'^password_change_company/$', views_company.password_change_company, name='password_change_company'),
    url(r'^companyeditprofile/(?P<companyid>\d+)$', views_company.company_edit_profile, name='editcompanyprofile'),
    url(r'^companyeventsandstatus/$', views_company.company_eventsandstatus, name='companyeventsandstatus'),
    url(r'^companycandidates/(?P<jobid>\d+)$', views_company.company_candidates, name='companycandidates'),
    # Job Actions : Students
    url(r'^jobaction/(?P<jobid>(\d+))/(?P<studid>(\d+))/$', views_company.job_stud_relation, name="jobaction"),
    url(r'^job_shortlist/(?P<relationid>\d+)$', views_company.job_shortlist, name='shortlist'),
    url(r'^job_unshortlist/(?P<relationid>\d+)$', views_company.job_unshortlist, name='unshortlist'),
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
    url(r'^companyrequestevent/$', views.company_requestevent, name='companyrequestevent'),
    # ----------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------
    # ADMINISTRATOR
    # ADMINISTRATOR
    # ADMINISTRATOR
    # ADMINISTRATOR
    # ADMINISTRATOR
    # ADMINISTRATOR
    # ADMINISTRATOR
    # ADMINISTRATOR
    # ADMINISTRATOR
    url(r'^admin_home/', views_admin.admin_home, name="admin_home"),
    url(r'^admin_logout/$', views_admin.admin_logout, name='admin_logout'),
    # Approve, sent_back & block

    url(r'^approve_job/(?P<jobid>\d+)$', views_admin.approve_job, name='approve_job'),
    # url(r'^sent_back_job/(?P<jobid>\d+)$', views_admin.sent_back_job, name='sent_back_job'),
    url(r'^admin_approval/(?P<object_type>[A-Za-z_]+)$', views_admin.admin_approvals, name='admin_approval'),
    # Search Users
    url(r'admin_manage/$', views_admin.admin_manage, name="admin_manage"),
    url(r'^search_students/$', views_admin.search_students, name='search_students'),
    url(r'^add_student/$', views_admin.add_student, name='add_student'),
    url(r'^add_company/$', views_admin.add_company, name='add_company'),
    url(r'^review_stud_profile/(?P<studid>\d+)$', views_admin.review_stud_profile, name='review_stud_profile'),
    url(r'^edit_student/(?P<studid>\d+)$', views_admin.edit_student, name='edit_student'),
    # Requests
    url(r'^signup_requests/$', views_admin.signup_requests, name='signup_requests'),
    url(r'^add_company_by_signup_request/(?P<companyregid>\d+)$', views_admin.add_company_by_signup_request,
        name='add_company_by_signup_request'),
    url(r'^review_request_profile/(?P<companyregid>\d+)$', views_admin.review_request_profile,
        name='review_request_profile'),
    url(r'^del_signup_request/(?P<companyregid>\d+)$', views_admin.del_signup_request, name='del_signup_request'),
    # companies
    url(r'^companies/$', views_admin.companies, name='companies'),
    url(r'^delete_company/(?P<companyid>\d+)$', views_admin.delete_company, name='delete_company'),
    url(r'^add_company/(?P<companyid>\d+)$', views_admin.add_company, name='add_company'),
    url(r'^review_company_profile/(?P<companyid>\d+)$', views_admin.review_company_profile,
        name='review_company_profile'),
    url(r'^edit_company/(?P<companyid>\d+)$', views_admin.edit_company, name='edit_company'),
    # Jobs
    url(r'^jobs/$', views_admin.jobs, name='jobs'),
    url(r'^review_job/(?P<jobid>\d+)$', views_admin.review_job, name='review_job'),
    url(r'^edit_progs/(?P<jobid>\d+)$', views_admin.edit_progs, name='edit_progs'),
    url(r'^edit_job/(?P<jobid>\d+)$', views_admin.edit_job, name='edit_job'),
    url(r'^delete_job/(?P<jobid>\d+)$', views_admin.delete_job, name='delete_job'),
    url(r'^job_candidates/(?P<jobid>\d+)$', views_admin.job_candidates, name='job_candidates'),
    url(r'^approve_action/(?P<applicant_type>[A-za-z]+)/(?P<relationid>\d+)$', views_admin.approve_action,
        name='approve_action'),
    url(r'^approve_stud_relation/(?P<relationid>\d+)$', views_admin.approve_stud_relation, name='approve_stud'),
    # departments
    url(r'departments/$', views_admin.departments, name="departments"),
    url(r'add_department/$', views_admin.add_department, name="add_department"),
    url(r'^edit_department/(?P<deptid>\d+)$', views_admin.edit_department, name='edit_department'),
    url(r'^delete_department/(?P<deptid>\d+)$', views_admin.delete_department, name='delete_department'),
    # programmes
    url(r'^programmes/$', views_admin.programmes, name="programmes"),
    url(r'add_programme/$', views_admin.add_programme, name="add_programme"),
    url(r'^edit_programme/(?P<progid>\d+)$', views_admin.edit_programme, name='edit_programme'),
    url(r'^delete_programme/(?P<progid>\d+)$', views_admin.delete_programme, name='delete_programme'),
    # Years
    url(r'^years/$', views_admin.years, name="years"),
    url(r'add_year/$', views_admin.add_year, name="add_year"),
    url(r'^delete_year/(?P<yearid>\d+)$', views_admin.delete_year, name='delete_year'),
]
