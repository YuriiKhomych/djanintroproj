from django.conf.urls import url

from events.views import events_list, single_event, add_event, join_member

urlpatterns = [
    url(r'^$', events_list, name='all_events'),
    url(r'^add-event/$', add_event, name='add_event'),
    url(r'^single/(?P<event_id>\d+)/$', single_event, name='single_event_page'),
    url(r'^single/(?P<event_id>\d+)/join-member/$', join_member, name='join_member'),
]

