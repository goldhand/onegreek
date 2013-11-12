# -*- coding: utf-8 -*-
from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Fraternity


admin.site.register(Fraternity)