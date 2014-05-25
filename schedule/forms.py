from django import forms
from django.utils.translation import ugettext_lazy as _
from schedule.models import Event, Occurrence, CalendarPluginModel


class SpanForm(forms.ModelForm):
    start = forms.DateTimeField(label=_("start"),
                                widget=forms.SplitDateTimeWidget)
    end = forms.DateTimeField(label=_("end"),
                              widget=forms.SplitDateTimeWidget,
                              help_text=_(u"The end time must be later than start time."))

    def clean(self):
        if 'end' in self.cleaned_data and 'start' in self.cleaned_data:
            if self.cleaned_data['end'] <= self.cleaned_data['start']:
                raise forms.ValidationError(_(u"The end time must be later than start time."))
        return self.cleaned_data


class EventForm(SpanForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

    end_recurring_period = forms.DateTimeField(label=_(u"End recurring period"),
                                               help_text=_(u"This date is ignored for one time only events."),
                                               required=False)

    class Meta:
        model = Event
        exclude = ('creator', 'created_on', 'calendar')


class OccurrenceForm(SpanForm):
    class Meta:
        model = Occurrence
        exclude = ('original_start', 'original_end', 'event', 'cancelled')


class CalendarPluginForm(forms.ModelForm):
    class Meta:
        model = CalendarPluginModel

    def __init__(self, *args, **kwargs):
        # Limit the calendar queryset to ones that have a site same as the page it's being put on
        self.request = kwargs.pop('request', None)
        super(CalendarPluginForm, self).__init__(*args, **kwargs)
        try:
            page_site = self.request.user.userprofile.site
        except:
            page_site = None
        if page_site:
            self.fields['calendar'].queryset = self.fields['calendar'].queryset.filter(site=page_site)
        if len(self.fields['calendar'].queryset) == 1:
            self.fields['calendar'].initial = self.fields['calendar'].queryset[0]
