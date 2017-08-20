from django.conf.urls import url

from trips.views import SingleTrip, AddTrip, AllTrips, JoinTrip


urlpatterns = [
    url(r'^add-road-trip/$', AddTrip.as_view(), name='add_trip'),
    url(r'^$', AllTrips.as_view(), name='all_trips'),
    url(r'^single/(?P<trip_id>\d+)/$', SingleTrip.as_view(), name='single_trip_page'),
    url(r'^single/(?P<trip_id>\d+)/join-passenger/$', JoinTrip.as_view(), name='join_passenger'),
]
