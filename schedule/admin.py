from django.contrib import admin

from schedule.models import Calendar, Event, CalendarRelation, Rule


class CalendarAdminOptions(admin.ModelAdmin):
    list_display = ('name', 'slug', 'site')
    list_filter = ('site',)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class EventAdminOptions(admin.ModelAdmin):
    list_display = ('start', 'title', 'calendar')
    list_filter = ('calendar', 'calendar__site')
    ordering = ('-start',)


admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(Event, EventAdminOptions)
admin.site.register([Rule, CalendarRelation])
