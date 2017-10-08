from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import View

from blog.models import Article
from blog.forms import SearchForm, CreateNewArticle

from utils import gen_page_list


class Home(View):

    def get(self, request):
        form = SearchForm(request.GET)
        if form.is_valid():
            # data = form.cleaned_data
            keyword = request.GET.get('search_text', '')
            # How do it? (title__contains=data.get(keyword))
            articles = Article.objects.filter(title__contains=keyword)
        else:
            form = SearchForm()
            articles = Article.objects.order_by('-added').all()
        # pagination part
        page = request.GET.get('page', 1)
        p = Paginator(articles, 5)
        try:
            final_articles = p.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            final_articles = p.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            final_articles = p.page(p.num_pages)
        return render(request,
                      'blogs.html',
                      {'articles': final_articles,
                       'form': form,
                       'pagination': gen_page_list(page, p.num_pages)})


class SingleBlog(View):
    def get(self, request, article_id):
        # try:
        #     # select * from blog_article where id = 2
        #     article = Article.objects.get(id=article_id)
        #     return render(request, 'single-blog.html', {'article': article})
        # except Article.DoesNotExist:
        #     raise Http404
        article = get_object_or_404(Article, id=article_id)
        return render(request, 'single-blog.html', {'article': article})


class UserArticles(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        articles = Article.objects.filter(author=user)
        return render(request, 'user-blog.html', {'articles': articles,
                                                  'user': user})


class ArticleLike(View):
    def get(self, request, article_id):
        if request.user.is_authenticated:
            article = get_object_or_404(Article, id=article_id)
            if request.user in article.liked_by.all():
                article.liked_by.remove(request.user)
            else:
                article.liked_by.add(request.user)
            article.save()
            return HttpResponseRedirect(reverse('all_articles'))
        else:
            return HttpResponseRedirect(reverse('sign_up'))


class AddArticle(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'add_article.html', {'form': CreateNewArticle})
        else:
            return HttpResponseRedirect(reverse('sign_up'))

    def post(self, request):
        form = CreateNewArticle(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.published_date = timezone.now()
            article.save()
            return redirect('single_article_page', article_id=article.pk)
        return render(request, 'add_article.html', {'form': form})
