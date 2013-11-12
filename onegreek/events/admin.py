from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Event


class EventAdmin(GuardedModelAdmin):
    pass

admin.site.register(Event, EventAdmin)