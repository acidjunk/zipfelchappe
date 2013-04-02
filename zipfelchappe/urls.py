from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$',
        views.ProjectListView.as_view(),
        name='zipfelchappe_project_list'),
    url(r'^project/(?P<slug>[\w-]+)/$',
        views.ProjectDetailView.as_view(),
        name='zipfelchappe_project_detail'),
    url(r'^project/(?P<slug>[\w-]+)/update/(?P<pk>\d+)/$',
        views.UpdateDetailView.as_view(),
        name='zipfelchappe_update_detail'),
    url(r'^category/(?P<slug>[\w-]+)/',
        views.ProjectCategoryListView.as_view(),
        name='zipfelchappe_project_category_list'),
    url(r'^back/(?P<slug>[\w-]+)/$',
        views.project_back_form,
        name='zipfelchappe_project_back_form'),

    url(r'^backer/authenticate/$',
        views.backer_authenticate,
        name='zipfelchappe_backer_authenticate'),
    url(r'^backer/login/$',
        views.BackerLoginView.as_view(),
        name='zipfelchappe_backer_login'),
    url(r'^backer/register/$',
        views.BackerRegisterView.as_view(),
        name='zipfelchappe_backer_register'),


    url(r'^pledge/thankyou/$',
        views.pledge_thankyou,
        name='zipfelchappe_pledge_thankyou'),
    url(r'^pledge/cancel/$',
        views.pledge_cancel,
        name='zipfelchappe_pledge_cancel'),
    url(r'^pledge/lost/$',
        views.PledgeLostView.as_view(),
        name='zipfelchappe_pledge_lost'),
)
