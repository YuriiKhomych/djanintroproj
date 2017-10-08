from django.conf.urls import url

from .views import (
    ChangeUserPasswordView,
    MainUserFieldsView, UsersView,
    UserLoginAPI, UserRegistrationAPI, UserForgetPasswordAPI,
    UserShortInfoAPI,
)

urlpatterns = [
    # accounts API
    url(r'^users-rest/$', UsersView.as_view()),
    url(r'^main-user-info/$', MainUserFieldsView.as_view()),
    url(r'^user-short-info-api/$', UserShortInfoAPI.as_view()),
    url(r'^change-user-password-rest/$', ChangeUserPasswordView.as_view()),
    url(r'^users-rest/(?P<pk>\d+)/$', UsersView.as_view()),
    url(r'^login-api/$', UserLoginAPI.as_view()),
    url(r'^user-registration-api/$', UserRegistrationAPI.as_view()),
    url(r'^user-forget-password-api/$', UserForgetPasswordAPI.as_view()),
]
