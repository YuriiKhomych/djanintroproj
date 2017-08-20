from django.shortcuts import render, get_object_or_404, redirect,\
    HttpResponseRedirect, reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.views.generic import View

from trips.models import Trip
from .forms import CreateNewTrip

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
            trip = get_object_or_404(Trip, id=trip_id)
            return render(request, 'single-trip.html', {'trip': trip})
        else:
            return HttpResponseRedirect(reverse('sign_up'))


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
