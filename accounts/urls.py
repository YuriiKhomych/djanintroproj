from django.conf.urls import url

from accounts.views import AllUsers, SingleUser, SignIn, SignOut, SignUp

urlpatterns = [
    url(r'^sign-in/$', SignIn.as_view(), name='sign_in'),
    url(r'^sign-out/$', SignOut.as_view(), name='sign_out'),
    url(r'^sign-up/$', SignUp.as_view(), name='sign_up'),
    url(r'^users/$', AllUsers.as_view(), name='all_users'),
    url(r'^single/(?P<user_id>\d+)/$', SingleUser.as_view(), name='single_user_page'),
]
