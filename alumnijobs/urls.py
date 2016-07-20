from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^rec_add_alum_job$', views.company_add_job, name='rec_add_alum_job'),
    url(r'^rec_all_alum_jobs$', views.company_all_alum_jobs, name='rec_all_alum_jobs'),
    url(r'^rec_alum_job_details/(?P<jobid>\d+)$', views.company_alum_job_details, name='rec_alum_job_details'),
    url(r'^rec_edit_alum_job/(?P<jobid>\d+)$', views.company_edit_alum_job, name='rec_edit_alum_job'),
    url(r'^rec_alum_job_all_candidates/(?P<jobid>\d+)$', views.company_alum_job_candidates,
        name='rec_alum_job_all_candidates'),

    url(r'^alum_all_alum_jobs$', views.alum_all_jobs, name='alum_all_alum_jobs'),
    url(r'^alum_alum_job_details/(?P<jobid>\d+)$', views.alum_alum_job_details, name='alum_alum_job_details'),
    url(r'^alum_alum_job_apply/(?P<jobid>\d+)$', views.alum_alum_job_apply, name='alum_alum_job_apply'),
    url(r'^alum_alum_job_deapply/(?P<jobid>\d+)$', views.alum_alum_job_deapply, name='alum_alum_job_deapply'),

    url(r'^admin_all_alum_jobs$', views.admin_all_alum_jobs, name='admin_all_alum_jobs'),
    url(r'^admin_alum_job_details/(?P<jobid>\d+)$', views.admin_alum_job_details, name='admin_alum_job_details'),
    url(r'^admin_edit_alum_job/(?P<jobid>\d+)$', views.admin_edit_alum_job, name='admin_edit_alum_job'),
]
