from django.conf.urls import url

from trips.views import SingleTrip, AddTrip, AllTrips, JoinTrip, DelComment, EditComment


urlpatterns = [
    url(r'^add-road-trip/$', AddTrip.as_view(), name='add_trip'),
    url(r'^$', AllTrips.as_view(), name='all_trips'),
    url(r'^single/(?P<trip_id>\d+)/$', SingleTrip.as_view(), name='single_trip_page'),
    url(r'^single/(?P<trip_id>\d+)/join-passenger/$', JoinTrip.as_view(), name='join_passenger'),
    url(r'^delcomment/(?P<comment_id>[\d]+)/$', DelComment.as_view(), name="delete_comment"),
    url(r'^editcomment/(?P<comment_id>[\d]+)/$', EditComment.as_view(), name="edit_comment"),
]
