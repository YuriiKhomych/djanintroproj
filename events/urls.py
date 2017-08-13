from django.conf.urls import url

from events.views import events_list, single_event, add_event

urlpatterns = [
    url(r'^add-event/$', add_event, name='add_event'),
    url(r'^$', events_list, name='all_events'),
    url(r'^single/(?P<event_id>\d+)/$', single_event, name='single_event_page'),
]

