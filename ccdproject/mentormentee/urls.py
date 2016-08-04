from django.conf.urls import url

from . import views

urlpatterns = [

    # Add a new proposal
    url(r'^add_proposal$', views.add_research_proposal, name='add_proposal'),
    # View all posted proposals
    url(r'^alum_proposals$', views.alum_proposals, name='alum_proposals'),
    # Edit proposals
    url(r'^edit_proposals/(?P<proposalid>\d+)$', views.edit_proposal, name='edit_proposal'),
    # Delete
    url(r'^del_proposals/(?P<proposalid>\d+)$', views.delete_proposal, name='delete_proposal'),
    # Applicants
    url(r'^applicants/(?P<proposalid>\d+)$', views.applicants, name='applicants'),
    # Review proposal
    url(r'^alum_review_proposal/(?P<proposalid>\d+)$', views.alum_review_proposal, name='alum_review_proposal'),
    # Review Applicants
    url(r'^review_applicant/(?P<proposalid>\d+)/(?P<studid>\d+)$', views.review_applicant, name='review_applicant'),
    # Report
    url(r'^report_stud/(?P<relationid>\d+)', views.report_stud, name="report_stud"),


    # All proposals
    url(r'stud_proposals/$', views.stud_proposals, name="stud_proposals"),
    # Review proposal
    url(r'^stud_review_proposal/(?P<proposalid>\d+)$', views.stud_review_proposal, name='stud_review_proposal'),
    # Apply
    url(r'stud_apply/(?P<proposalid>\d+)$', views.stud_apply, name="stud_apply"),
    # Opt out
    url(r'opt_out/(?P<relationid>\d+)$', views.opt_out, name="opt_out"),
    # Report
    url(r'^report_alum/(?P<relationid>\d+)', views.report_alum, name="report_alum"),
]
