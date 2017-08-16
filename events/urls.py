from django.conf.urls import url

from events.views import SingleEvent, AddEvent, AllEvents, JoinEvent


urlpatterns = [
    url(r'^add-event/$', AddEvent.as_view(), name='add_event'),
    url(r'^$', AllEvents.as_view(), name='all_events'),
    url(r'^single/(?P<event_id>\d+)/$', SingleEvent.as_view(), name='single_event_page'),
    url(r'^single/(?P<event_id>\d+)/join-member/$', JoinEvent.as_view(), name='join_member'),
]
