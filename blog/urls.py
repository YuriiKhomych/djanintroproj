from django.conf.urls import url

from blog.views import Home, SingleBlog, UserArticles, AddArticle, ArticleLike

urlpatterns = [
    url(r'^$', Home.as_view(), name='all_articles'),
    url(r'^new/$', AddArticle.as_view(), name='add_article'),
    url(r'^single/(?P<article_id>\d+)/$', SingleBlog.as_view(),
        name='single_article_page'),
    url(r'^single/(?P<article_id>\d+)/like/$', ArticleLike.as_view(),
        name='like_article'),
    url(r'^user/(?P<user_id>\d+)/$', UserArticles.as_view(),
        name='user_articles'),
]
