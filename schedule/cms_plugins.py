from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import CalendarPluginForm
from .models.calendars import CalendarPluginModel


class CalendarCMSPluginBase(CMSPluginBase):
    form = CalendarPluginForm

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(CalendarCMSPluginBase, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return ModelFormMetaClass


class CalendarPlugin(CalendarCMSPluginBase):
    model = CalendarPluginModel
    name = ('Calendar')
    render_template = 'schedule/plugin_calendar.html'

plugin_pool.register_plugin(CalendarPlugin)
