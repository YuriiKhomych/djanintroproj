from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.views.generic import View

from accounts.forms import LoginForm, SignUpForm
from accounts.models import User

from utils import gen_page_list


class AllUsers(View):

    def get(self, request):
        page = request.GET.get('page', 1)
        paginator = Paginator(User.objects.all(), 10)
        try:
            page_come = paginator.page(page)
        except PageNotAnInteger:
            page_come = paginator.page(1)
        except EmptyPage:
            page_come = paginator.page(paginator.num_pages)
        return render(request, 'users.html', {
            'users': page_come,
            'pagination': gen_page_list(page, paginator.num_pages)
        })


class SingleUser(View):

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, 'single-user.html', {'user': user})


class SignIn(View):

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('all_articles'))
        else:
            form = LoginForm()
            return render(request, 'sign-in.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                email=data.get('email'),
                password=data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('all_articles'))
        return render(request, 'sign-in.html', {'form': form})


class SignOut(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('sign_in'))


class SignUp(View):

    def get(self, request):
        return render(request, 'sign-up.html', {'form': SignUpForm})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            user = authenticate(email=data.get('email'),
                                password=data.get('password1'))
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('all_articles'))
        return render(request, 'sign-up.html', {'form': form})
