from django.conf.urls import url
from django.views.generic import TemplateView

from . import (views, views_admin, views_company, views_alumni, views_print,
               views_verifier)

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='jobportal/index.html'),
    #     name='index'),
    url(r'^$', views.Login.as_view(), name='index'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),

    url(r'^stud/home/$', views.HomeView.as_view(), name='stud-home'),
    url(r'^stud/profile/detail/$', views.ProfileDetail.as_view(),
        name='stud-profile-detail'),
    url(r'^stud/profile/update/$', views.ProfileUpdate.as_view(),
        name='stud-profile-update'),

    url(r'^stud/job/all/list/$', views.AllJobList.as_view(),
        name='stud-all-job-list'),
    url(r'^stud/job/all/(?P<pk>\d+)/detail/$', views.AllJobDetail.as_view(),
        name='stud-all-job-detail'),

    url(r'^stud/job/eligible/list/$', views.JobList.as_view(),
        name='stud-job-list'),
    url(r'^stud/job/eligible/(?P<pk>\d+)/detail/$', views.JobDetail.as_view(),
        name='stud-job-detail'),

    url(r'^stud/jobrel/list/$', views.JobRelList.as_view(),
        name='stud-jobrel-list'),
    url(r'^stud/job/(?P<pk>\d+)/apply$', views.JobRelCreate.as_view(),
        name='stud-jobrel-create'),
    url(r'^stud/job/(?P<pk>\d+)/deapply$', views.JobRelDelete.as_view(),
        name='stud-jobrel-delete'),

    url(r'^stud/cv/$', views.CVDetail.as_view(), name='stud-cv-detail'),
    url(r'^stud/cv/create/$', views.CVCreate.as_view(), name='stud-cv-create'),
    url(r'^stud/cv/update/$', views.CVUpdate.as_view(), name='stud-cv-update'),
    url(r'^stud/cv/(?P<cvno>\d+)/download/$', views.DownloadCV.as_view(),
        name='stud-cv-download'),

    url(r'^stud/event/list/$', views.EventList.as_view(),
        name='stud-event-list'),
    url(r'^stud/event/<?pk>/detail$', views.EventDetail.as_view(),
        name='stud-event-detail'),

    url(r'^stud/avatar/detail/$', views.AvatarDetail.as_view(),
        name='stud-avatar-detail'),
    url(r'^stud/avatar/create/$', views.AvatarCreate.as_view(),
        name='stud-avatar-create'),
    url(r'^stud/avatar/update/$', views.AvatarUpdate.as_view(),
        name='stud-avatar-update'),

    url(r'^stud/sign/detail/$', views.SignatureDetail.as_view(),
        name='stud-sign-detail'),
    url(r'^stud/sign/create/$', views.SignatureCreate.as_view(),
        name='stud-sign-create'),
    url(r'^stud/sign/update/$', views.SignatureUpdate.as_view(),
        name='stud-sign-update'),

    url(r'^stud/announcement/list/$', views.AnnouncementList.as_view(),
        name='stud-announcement-list'),

    url(r'^signup/$', views_company.CompanySignUpView.as_view(),
        name='sigup'),
    url(r'^company/signup/$', views_company.CompanySignUpView.as_view(),
        name='company-signup'),
    url(r'^company/signupconfirm/$', TemplateView.as_view(
        template_name='jobportal/Company/signupconfirm.html'),
        name='signup-confirm'),
    url(r'^company/home/$', views_company.HomeView.as_view(),
        name='company-home'),

    url(r'^company/password/update/$',
        views_company.PasswordChangeView.as_view(),
        name='company-password-update'),
    url(r'^company/profile/detail/$', views_company.ProfileDetail.as_view(),
        name='company-profile-detail'),
    url(r'^company/profile/update/$', views_company.ProfileUpdate.as_view(),
        name='company-profile-update'),

    url(r'^company/programme/list/$', views_company.ProgrammeList.as_view(),
        name='company-programme-list'),

    url(r'^company/job/list/$', views_company.JobList.as_view(),
        name='company-job-list'),
    url(r'^company/job/create/$', views_company.JobCreate.as_view(),
        name='company-job-create'),
    url(r'^company/job/(?P<pk>\d+)/detail/$',
        views_company.JobDetail.as_view(), name='company-job-detail'),
    url(r'^company/job/(?P<pk>\d+)/update/$',
        views_company.JobUpdate.as_view(), name='company-job-update'),
    url(r'^company/job/(?P<pk>\d+)/download/bond/$',
        views_company.DownloadBondDocument.as_view(),
        name='company-job-download-bond'),

    url(r'^company/job/(?P<pk>\d+)/jobrel/list/$',
        views_company.JobRelList.as_view(), name='company-jobrel-list'),
    url(r'^company/job/(?P<jobpk>\d+)/jobrel/(?P<pk>\d+)/list/$',
        views_company.JobRelUpdate.as_view(), name='company-jobrel-update'),
    url(r'company/jobrel/(?P<pk>\d+)/cv/(?P<cvno>\d+)',
        views_company.DownloadStudCV.as_view(), name='company-jobrel-cv'),
    url(r'company/job/(?P<jobpk>\d+)/jobrel/(?P<jobrelpk>\d+)/shortlist',
        views_company.StudJobRelShortlist.as_view(),
        name='company-jobrel-shortlist'),
    url(r'company/job/(?P<jobpk>\d+)/jobrel/(?P<jobrelpk>\d+)/place',
        views_company.StudJobRelPlace.as_view(), name='company-jobrel-place'),
    url(r'company/job/(?P<jobpk>\d+)/jobrel/create/',
        views_company.JobProgrammeCreate.as_view(),
        name='company-job-jobprog-create'),


    url(r'^company/event/list/$', views_company.EventList.as_view(),
        name='company-event-list'),
    url(r'^company/event/create/$', views_company.EventCreate.as_view(),
        name='company-event-create'),
    url(r'^company/event/(?P<pk>\d+)/update/$',
        views_company.EventUpdate.as_view(), name='company-event-update'),
    url(r'^company/event/(?P<pk>\d+)/detail/$',
        views_company.EventDetail.as_view(), name='company-event-detail'),

    # File Downloads
    url(r'^download_cvs/(?P<jobid>\d+)$', views_company.download_cvs,
        name="download_cvs"),

    url(r'^admin/home/$', views_admin.HomeView.as_view(), name="admin-home"),

    url(r'^admin/student/create/', views_admin.UploadStudentData.as_view(),
        name='admin-student-create'),
    url(r'^admin/student/fee/update/',
        views_admin.StudentFeeStatusView.as_view(),
        name='admin-student-fee-update'),
    url(r'^admin/student/list/$', views_admin.StudentList.as_view(),
        name='admin-student-list'),
    url(r'^admin/student/(?P<pk>\d+)/detail/$',
        views_admin.StudentDetail.as_view(), name='admin-student-detail'),
    url(r'^admin/student/(?P<pk>\d+)/cv/(?P<cvno>\d+)/$',
        views_admin.DownloadStudCV.as_view(),
        name='admin-student-cv-download'),

    url(r'^admin/company/signup/list/$',
        views_admin.CompanySignupList.as_view(),
        name='admin-company-signup-list'),
    url(r'^admin/company/(?P<pk>\d+)/approve/$',
        views_admin.CompanyApprove.as_view(), name='admin-company-approve'),

    url(r'^admin/company/list/$', views_admin.CompanyList.as_view(),
        name='admin-company-list'),
    url(r'^admin/company/(?P<pk>\d+)/detail/$',
        views_admin.CompanyDetail.as_view(), name='admin-company-detail'),
    url(r'^admin/company/(?P<pk>\d+)/update/$',
        views_admin.CompanyUpdate.as_view(), name='admin-company-update'),

    url(r'^admin/job/list/$', views_admin.JobList.as_view(),
        name='admin-job-list'),
    url(r'^admin/job/list/unapproved$',
        views_admin.JobListUnapproved.as_view(),
        name='admin-job-list-unapproved'),
    url(r'^admin/job/(?P<pk>\d+)/detail/$',
        views_admin.JobDetail.as_view(), name='admin-job-detail'),
    url(r'^admin/job/(?P<pk>\d+)/update/$',
        views_admin.JobUpdate.as_view(), name='admin-job-update'),
    url(r'^admin/job/(?P<pk>\d+)/download/bond/$',
        views_admin.DownloadBondDocument.as_view(),
        name='admin-job-download-bond'),
    url(r'^admin/job/(?P<pk>\d+)/approve/$',
        views_admin.JobApprove.as_view(), name='admin-job-approve'),
    url(r'^admin/job/(?P<jobpk>\d+)/jobprog/list/update',
        views_admin.JobProgrammeUpdate.as_view(),
        name='admin-job-jobprog-list-update'),

    url(r'^admin/jobrel/list/unapproved/$',
        views_admin.JobRelListUnapproved.as_view(),
        name='admin-jobrel-list-unapproved'),
    url(r'^admin/job/(?P<pk>\d+)/jobrel/list/$',
        views_admin.JobRelList.as_view(), name='admin-jobrel-list'),
    url(r'^admin/job/(?P<jobpk>\d+)/jobrel/(?P<jobrelpk>\d+)/place/approve',
        views_admin.StudJobRelPlaceApprove.as_view(),
        name='admin-jobrel-place-approve'),

    url(r'^admin/event/list/$', views_admin.EventList.as_view(),
        name='admin-event-list'),
    url(r'^admin/event/(?P<pk>\d+)/detail/$',
        views_admin.EventDetail.as_view(), name='admin-event-detail'),
    url(r'^admin/event/(?P<pk>\d+)/update/$',
        views_admin.EventUpdate.as_view(), name='admin-event-update'),

    url(r'^admin/programme/list/$', views_admin.ProgrammeList.as_view(),
        name="programme-list"),
    url(r'^admin/programme/create/$', views_admin.ProgrammeCreate.as_view(),
        name="programme-create"),
    url(r'^admin/programme/(?P<pk>\d+)/update/$',
        views_admin.ProgrammeUpdate.as_view(), name='programme-update'),

    url(r'^admin/programme/placement/list/$',
        views_admin.ProgrammePlacementList.as_view(),
        name='admin-programme-placement-list'),
    url(r'^admin/programme/internship/list/$',
        views_admin.ProgrammeInternshipList.as_view(),
        name='admin-programme-internship-list'),

    url(r'^printcsv/(?P<jobid>\d+)$', views_print.candidates_stud_csv,
        name='printcsv'),
    url(r'^companies_csv/$', views_print.companies_csv, name='companies_csv'),
    url(r'^admin/stud/list/download/$', views_admin.DownloadStudList.as_view(),
        name='admin-stud-list-download'),
    url(r'^admin/company/list/download/$',
        views_admin.DownloadCompanyList.as_view(),
        name='admin-company-list-download'),

    url(r'^verifier/home/$', views_verifier.Home.as_view(),
        name="verifier-home"),
    url(r'^verifier/student/(?P<studid>\d+)/detail/$',
        views_verifier.StudentDetail.as_view(),
        name="verifier-student-detail"),
    url(r'^verifier/student/(?P<studid>\d+)/update/$',
        views_verifier.StudentUpdate.as_view(),
        name="verifier-student-update"),
    url(r'^verifier/student/(?P<studid>\d+)/cv/update/$',
        views_verifier.CVUpdate.as_view(),
        name="verifier-cv-update"),
    url(r'^verifier/student/(?P<studid>\d+)/cv/(?P<cvno>\d+)/$',
        views_verifier.StudentCVDownload.as_view(),
        name='verifier-student-cv-download'),
]
