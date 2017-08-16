from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.views.generic import View

from events.models import Event
from .forms import CreateNewEvent

from utils import gen_page_list


class AllEvents(View):

    def get(self, request):
        event = Event.objects.all()
        page = request.GET.get('page', 1)
        p = Paginator(event, 1)
        try:
            final_events = p.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            final_events = p.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            final_events = p.page(p.num_pages)
        return render(request,
                      'events.html',
                      {'events': final_events,
                       'pagination': gen_page_list(page, p.num_pages)})


class SingleEvent(View):

    def get(self ,request, event_id):
        event = get_object_or_404(Event, id=event_id)
        return render(request, 'single-event.html', {'event': event})


class JoinEvent(View):

    def get(self, request, event_id):
        if request.user.is_authenticated:
            event = get_object_or_404(Event, id=event_id)
            if request.user in event.members.all():
                event.members.remove(request.user)
            else:
                event.members.add(request.user)
                event.save()
            return HttpResponseRedirect(reverse('single_event_page',
                                                kwargs={'event_id': event_id}))
        else:
            return HttpResponseRedirect(reverse('sign_up'))


class AddEvent(View):

    def get(self, request):
        return render(request, 'add-event.html', {'form': CreateNewEvent})

    def post(self, request):
        form = CreateNewEvent(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.date = timezone.now()
            event.save()
            return redirect('all_events')
        return render(request, 'add-event.html', {'form': form})
