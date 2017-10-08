from django.conf.urls import url

from .views import get_user_django, get_user_rest, \
    change_user_password, ChangeUserPasswordView, \
    MainUserFieldsView, UsersView, UserCreateView, \
    UserLoginAPI, UserRegistrationAPI, UserForgetPasswordAPI, \
    UserShortInfoAPI, UserChangePasswordAPI

urlpatterns = [
    # accounts API
    url(r'^get-user-django/$', get_user_django),
    url(r'^get-user-rest/$', get_user_rest),
    url(r'^change-user-password/$', change_user_password),
    url(r'^main-user-info/$', MainUserFieldsView.as_view()),
    url(r'^change-user-password-rest/$', ChangeUserPasswordView.as_view()),
    url(r'^users-rest/$', UsersView.as_view()),
    url(r'^users-rest/(?P<pk>\d+)/$', UsersView.as_view()),
    url(r'^user-create-rest/$', UserCreateView.as_view()),

    # My improved rest-framework
    url(r'^login-api/$', UserLoginAPI.as_view()),
    url(r'^user-registration-api/$', UserRegistrationAPI.as_view()),
    url(r'^user-forget-password-api/$', UserForgetPasswordAPI.as_view()),
    url(r'^user-short-info-api/$', UserShortInfoAPI.as_view()),
    url(r'^user-change-password-api/$', UserChangePasswordAPI.as_view()),
]
