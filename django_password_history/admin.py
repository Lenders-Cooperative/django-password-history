#
# Created on Tue Dec 21 2021
#
# Copyright (c) 2021 Lenders Cooperative, a division of Summit Technology Group, Inc.
#
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (
   UserPasswordHistory,
)


@admin.register(UserPasswordHistory)
class UserPasswordHistoryAdmin(admin.ModelAdmin):
    pass



