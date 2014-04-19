from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models.calendars import CalendarPluginModel


class CalendarPlugin(CMSPluginBase):
    model = CalendarPluginModel
    name = ('Calendar Plugin')
    render_template = 'schedule/plugin.html'

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context

plugin_pool.register_plugin(CalendarPlugin)
