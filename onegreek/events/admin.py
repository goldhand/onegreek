from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Event, Attendees


class AttendeesAdmin(admin.StackedInline):
    model = Attendees
    max_num = 1


class EventAdmin(GuardedModelAdmin):
    inlines = [AttendeesAdmin]

admin.site.register(Event, EventAdmin)