from django.conf.urls import url

from .views import (
    # account
    UserRegistrationAPI,
    UserShortInfoAPI,
    UsersViewAPI,
    UserLoginAPI,
    UserForgetPasswordAPI,
    ChangeUserPasswordAPI,
    # blog
    ArticlesView,
    ArticlesAllAPI,
    ArticleCreateAPI,
    ArticleRetrieveUpdateDestroyAPI,
    ArticlesSearchAPI,
    # trip
    TripView,
    TripAllAPI,
    TripCreateAPI,
    TripRetrieveUpdateDestroyAPI,
    TripSearchAPI
)

urlpatterns = [
    # accounts API
    url(r'^user-registration-api/$', UserRegistrationAPI.as_view()),
    url(r'^user-short-info-api/$', UserShortInfoAPI.as_view()),
    url(r'^users-rest/$', UsersViewAPI.as_view()),
    url(r'^users-rest/(?P<pk>\d+)/$', UsersViewAPI.as_view()),
    url(r'^login-api/$', UserLoginAPI.as_view()),
    url(r'^user-forget-password-api/$', UserForgetPasswordAPI.as_view()),
    url(r'^change-user-password-rest/$', ChangeUserPasswordAPI.as_view()),
    # blog API
    url(r'^articles-rest/$', ArticlesView.as_view()),
    url(r'^articles-rest/(?P<pk>\d+)/$', ArticlesView.as_view()),
    url(r'^articles-all-api/$', ArticlesAllAPI.as_view()),
    url(r'^articles-create-api/$', ArticleCreateAPI.as_view()),
    url(r'^articles-retrieve-update-destroy-api/(?P<pk>\d+)/$',
        ArticleRetrieveUpdateDestroyAPI.as_view()),
    url(r'^articles-search-api/$', ArticlesSearchAPI.as_view()),
    # trip API
    url(r'^trip-rest/$', TripView.as_view()),
    url(r'^trip-rest/(?P<pk>\d+)/$', TripView.as_view()),
    url(r'^trip-all-api/$', TripAllAPI.as_view()),
    url(r'^trip-create-api/$', TripCreateAPI.as_view()),
    url(r'^trip-retrieve-update-destroy-api/(?P<pk>\d+)/$',
        TripRetrieveUpdateDestroyAPI.as_view()),
    url(r'^trip-search-api/$', TripSearchAPI.as_view()),
]
