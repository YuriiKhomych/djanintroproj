from django.conf.urls import url

from blog.views import Home, SingleBlog, UserArticles, AddArticle,\
    send_email_rest, ArticlesView, ArticleLike,\
    ArticlesAllAPI,ArticleCreateAPI, \
    ArticleRemoveAPI, ArticlesSearchAPI

urlpatterns = [
    url(r'^$', Home.as_view(), name='all_articles'),
    url(r'^new/$', AddArticle.as_view(), name='add_article'),
    url(r'^single/(?P<article_id>\d+)/$', SingleBlog.as_view(),
        name='single_article_page'),
    url(r'^single/(?P<article_id>\d+)/like/$', ArticleLike.as_view(),
        name='like_article'),
    url(r'^user/(?P<user_id>\d+)/$', UserArticles.as_view(),
        name='user_articles'),

    # REST
    url(r'^send-email-rest/$', send_email_rest, name='send_email_rest'),
    url(r'^articles-rest/$', ArticlesView.as_view()),
    url(r'^articles-rest/(?P<pk>\d+)/$', ArticlesView.as_view()),

    # rest framework
    url(r'^articles-all-api/$', ArticlesAllAPI.as_view()),
    url(r'^articles-create-api/$', ArticleCreateAPI.as_view()),
    url(r'^articles-remove-api/$', ArticleRemoveAPI.as_view()),
    url(r'^articles-search-api/$', ArticlesSearchAPI.as_view()),
]


# /blog/ -> all blogs
# /blog/single/12345/ -> single blog
# /blog/user/123456/ -> single user(with all articles)