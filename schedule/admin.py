from django import forms
from django.contrib import admin

from schedule.models import Calendar, Event, CalendarRelation, Rule


class CalendarAdminOptions(admin.ModelAdmin):
    list_display = ('name', 'slug', 'site')
    list_filter = ('site',)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event

    def __init__(self, *args, **kwargs):
        # Limit calendar choice to request.user and pre-select
        self.request = kwargs.pop('request', None)
        super(EventAdminForm, self).__init__(*args, **kwargs)
        if not self.request.user.is_superuser:
            user_site = self.request.user.userprofile.site
            if not user_site:
                self.fields['calendar'].queryset = []
            self.fields['calendar'].queryset = self.fields['calendar'].queryset.filter(site=user_site)
            if len(self.fields['calendar'].queryset) == 1:
                self.fields['calendar'].initial = self.fields['calendar'].queryset[0]

    def save(self, *args, **kwargs):
        # Set creator to request.user
        self.instance.creator = self.request.user
        return super(EventAdminForm, self).save(*args, **kwargs)


class EventAdminOptions(admin.ModelAdmin):
    list_display = ('start', 'title', 'calendar', 'site')
    list_filter = ('calendar', 'calendar__site')
    ordering = ('-start',)
    exclude = ('creator', 'rule', 'end_recurring_period')

    form = EventAdminForm

    def get_form(self, request, obj=None, **kwargs):
        # Customise the save form
        AdminForm = super(EventAdminOptions, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return ModelFormMetaClass

    def queryset(self, request):
        # Only show users events for their own calendars (if not superuser)
        qs = super(EventAdminOptions, self).queryset(request)
        if not request.user.is_superuser:
            user_site = request.user.userprofile.site
            if not user_site:
                return []
            return qs.filter(calendar__site=user_site)
        return qs

    def get_list_filter(self, request):
        # Only superuser should see list of sites/calendars to filter
        if not request.user.is_superuser:
            return ()
        return self.list_filter

    def site(self, obj):
        return obj.calendar.site


admin.site.register(Calendar, CalendarAdminOptions)
admin.site.register(Event, EventAdminOptions)
admin.site.register([Rule, CalendarRelation])
