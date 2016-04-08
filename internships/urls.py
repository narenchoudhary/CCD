from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^rec_add_intern$', views.company_add_intern, name='rec_add_intern'),
    url(r'^rec_all_interns$', views.company_all_interns, name='rec_all_interns'),
    url(r'^rec_intern_details/(?P<internid>\d+)$', views.company_intern_details, name='rec_intern_details'),
    url(r'^rec_edit_intern/(?P<internid>\d+)$', views.company_edit_intern, name='rec_edit_intern'),
    url(r'^rec_add_progs/(?P<internid>\d+)$', views.company_add_progs, name='rec_add_progs'),
    url(r'^rec_intern_drop/(?P<internid>\d+)$', views.company_intern_drop, name='rec_intern_drop'),
    url(r'^rec_intern_candidates/(?P<internid>\d+)$', views.company_intern_candidates, name='rec_intern_candidates'),
    url(r'^rec_intern_rel/(?P<relid>\d+)$', views.company_intern_rel, name='rec_intern_rel'),
    url(r'^rec_intern_shortlist/(?P<relid>\d+)$', views.company_intern_shortlist, name='rec_intern_shortlist'),
    url(r'^rec_intern_intern/(?P<relid>\d+)$', views.company_intern_intern, name='rec_intern_intern'),
    url(r'^rec_intern_ppo/(?P<relid>\d+)$', views.company_intern_ppo, name='rec_intern_ppo'),

    url(r'^admin_all_interns$', views.admin_all_interns, name='admin_all_interns'),
    url(r'^admin_intern_details/(?P<internid>\d+)$', views.admin_intern_details, name='admin_intern_details'),
    url(r'^admin_edit_intern/(?P<internid>\d+)$', views.admin_edit_intern, name='admin_edit_intern'),
    url(r'^admin_delete_intern/(?P<internid>\d+)$', views.admin_delete_intern, name='admin_delete_intern'),
    url(r'^admin_add_progs/(?P<internid>\d+)$', views.admin_add_progs, name='admin_add_progs'),
    url(r'^admin_intern_candidates/(?P<internid>\d+)$', views.admin_intern_candidates, name='admin_intern_candidates'),
    url(r'^admin_intern_rel/(?P<relid>\d+)$', views.admin_rel_approvals, name='admin_intern_rel'),
    # shortlist
    url(r'^admin_intern_shortlist/(?P<relid>\d+)$', views.admin_approve_shortlist, name='admin_intern_shortlist'),
    url(r'^admin_reject_shortlist/(?P<relid>\d+)$', views.admin_reject_shortlist, name='admin_reject_shortlist'),
    # hire
    url(r'^admin_intern_intern/(?P<relid>\d+)$', views.admin_approve_intern, name='admin_intern_intern'),
    url(r'^admin_reject_intern/(?P<relid>\d+)$', views.admin_reject_intern, name='admin_reject_intern'),
    # ppo
    url(r'^admin_intern_ppo/(?P<relid>\d+)$', views.admin_approve_ppo, name='admin_intern_ppo'),
    url(r'^admin_reject_ppo/(?P<relid>\d+)$', views.admin_reject_ppo, name='admin_reject_ppo'),

    url(r'^stud_all_interns$', views.stud_all_interns, name='stud_all_interns'),
    url(r'^stud_intern_details/(?P<internid>\d+)$', views.stud_intern_details, name='stud_intern_details'),
    url(r'^stud_intern_apply/(?P<internid>\d+)$', views.stud_intern_apply, name='stud_intern_apply'),
    url(r'^stud_intern_deapply/(?P<internid>\d+)$', views.stud_intern_deapply, name='stud_intern_deapply'),
]
