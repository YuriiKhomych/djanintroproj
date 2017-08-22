from django.shortcuts import render, get_object_or_404, redirect,\
    HttpResponseRedirect, reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.views.generic import View
from django.db.utils import IntegrityError


from .models import Trip, Comment
from .forms import CreateNewTrip, CommentForm, AddToCartForm

from datetime import datetime

from utils import gen_page_list


class AllTrips(View):

    def get(self, request):
        trip = Trip.objects.all()
        page = request.GET.get('page', 1)
        p = Paginator(trip, 1)
        try:
            final_trips = p.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            final_trips = p.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            final_trips = p.page(p.num_pages)
        return render(request,
                      'trips.html',
                      {'trips': final_trips,
                       'pagination': gen_page_list(page, p.num_pages)})


class SingleTrip(View):

    def get(self ,request, trip_id):
        if request.user.is_authenticated:
            trip = get_object_or_404(Trip, pk=trip_id)
            trip.views += 1
            comments = Comment.objects.filter(trip_id=trip_id)
            rating = [float(i.rating) for i in comments]
            try:
                trip.rating = "{:.1f}".format(sum(rating) / len(rating))
            except ZeroDivisionError:
                trip.rating = 0
                trip.save()
            commentform = CommentForm()
            cartform = AddToCartForm()
            return render(request, 'single-trip.html',
                          {"trip": trip, "comments": comments,
                           "commentform": commentform, "cartform": cartform})
        else:
            return HttpResponseRedirect(reverse('sign_up'))



    def post(self, request, trip_id):
        commentform = CommentForm(request.POST)
        cartform = AddToCartForm()
        trip = get_object_or_404(Trip, pk=trip_id)
        comments = Comment.objects.filter(trip_id=trip_id)
        if commentform.is_valid():
            author = request.user
            trip = Trip.objects.get(pk=trip_id)
            pos = commentform.cleaned_data["positive"]
            neg = commentform.cleaned_data["negative"]
            body = commentform.cleaned_data["body"]
            rating = commentform.cleaned_data["rating"]
            comm = Comment(author=author,
                           trip=trip,
                           positive=pos,
                           negative=neg,
                           body=body,
                           rating=rating)
            try:
                comm.save()
            except IntegrityError:
                commentform.add_error("positive", "You already added the comment. Edit the existing one!")
        return render(request, "single-trip.html", {"trip": trip, "comments": comments,
                                                       "commentform": commentform, "cartform": cartform})

class JoinTrip(View):

    def get(self, request, trip_id):
        if request.user.is_authenticated:
            trip = get_object_or_404(Trip, id=trip_id)
            if request.user in trip.passengers.all():
                trip.passengers.remove(request.user)
            else:
                trip.passengers.add(request.user)
                trip.save()
            return HttpResponseRedirect(reverse('single_trip_page',
                                                kwargs={'trip_id': trip_id}))
        else:
            return HttpResponseRedirect(reverse('sign_up'))


class AddTrip(View):

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'add-trip.html', {'form': CreateNewTrip})
        else:
            return HttpResponseRedirect(reverse('sign_up'))

    def post(self, request):
        form = CreateNewTrip(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.driver = request.user
            trip.date = timezone.now()
            trip.save()
            return redirect('all_trips')
        return render(request, 'add-trip.html', {'form': form})


class DelComment(View):
    def get(self, request, comment_id):
        if request.user.is_authenticated:
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
        return HttpResponseRedirect('all_trips')


class EditComment(View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.author_id == request.user.id or request.user.is_admin:
            form = CommentForm(instance=comment)
            return render(request, "edit_comment.html", {"form": form, "comment": comment})
        HttpResponseRedirect(reverse("all_trips"))

    def post(self, request, comment_id):
        form = CommentForm(request.POST)
        comment_old = Comment.objects.get(pk=comment_id)
        if form.is_valid() and (request.user.is_admin or comment_old.author_id == request.user.id):
            comment_old.positive = form.cleaned_data["positive"]
            comment_old.negative = form.cleaned_data["negative"]
            comment_old.body = form.cleaned_data["body"]
            comment_old.rating = form.cleaned_data["rating"]
            comment_old.edit_amount += 1
            comment_old.edit_date = datetime.now()
            comment_old.save()
        return HttpResponseRedirect('all_trips')