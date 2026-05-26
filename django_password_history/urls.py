#
# Created on Tue Dec 21 2021
#
# Copyright (c) 2021 Lenders Cooperative, a division of Summit Technology Group, Inc.
#
# -*- coding: utf-8 -*-

from django.urls import re_path
from django.views.generic import TemplateView

from . import views


app_name = 'django_password_history'
urlpatterns = [
    re_path(
        r"^UserPasswordHistory/~create/$",
        views.UserPasswordHistoryCreateView.as_view(),
        name='UserPasswordHistory_create',
    ),
    re_path(
        r"^UserPasswordHistory/(?P<pk>\d+)/~delete/$",
        views.UserPasswordHistoryDeleteView.as_view(),
        name='UserPasswordHistory_delete',
    ),
    re_path(
        r"^UserPasswordHistory/(?P<pk>\d+)/$",
        views.UserPasswordHistoryDetailView.as_view(),
        name='UserPasswordHistory_detail',
    ),
    re_path(
        r"^UserPasswordHistory/(?P<pk>\d+)/~update/$",
        views.UserPasswordHistoryUpdateView.as_view(),
        name='UserPasswordHistory_update',
    ),
    re_path(
        r"^UserPasswordHistory/$",
        views.UserPasswordHistoryListView.as_view(),
        name='UserPasswordHistory_list',
    ),
	]
