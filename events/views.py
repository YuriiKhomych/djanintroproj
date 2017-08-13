from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone

from events.models import Event
from .forms import CreateNewEvent

from utils import gen_page_list


def events_list(request):
    event = Event.objects.order_by('-date').all()
    # event.members.add()
    # event.members.add(User.objects.get(email='test@gmail.com'))
    # event.members.remove(User.objects.get(email='test@gmail.com'))
    # event.save()
    # print(event.title)
    # event.title = 'new title'
    # event.save()
    # print(event.title)
    # print(event.date)
    # members = event.members.all()
    # for member in members:
    #     print(member.email)
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
    return render(request, 'events.html', {'events': final_events,
                                          'pagination': gen_page_list(page,p.num_pages)})


def single_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'single-event.html', {'event': event})


def add_event(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateNewEvent(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.creator = request.user
                event.date = timezone.now()
                event.save()
                return redirect('all_events')
        else:
            form = CreateNewEvent()
        return render(request, 'add-event.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('all_events'))


def join_member(request, event_id):
    if request.user.is_authenticated:
        event = get_object_or_404(Event, id=event_id)
        if request.user in event.members.all():
            event.members.remove(request.user)
        else:
            event.members.add(request.user)
            event.save()
        return HttpResponseRedirect(reverse('all_events'))
    else:
        return HttpResponseRedirect(reverse('sign_up'))

# class Event(View):
#     form_class = Event
#
#     def get(self, request):
#         event = self.form_class.objects.all()
#         page = request.GET.get('page', 1)
#         p = Paginator(event, 1)
#         try:
#             final_events = p.page(page)
#         except PageNotAnInteger:
#             # If page is not an integer, deliver first page.
#             final_events = p.page(1)
#         except EmptyPage:
#             # If page is out of range (e.g. 9999), deliver last page of results.
#             final_events = p.page(p.num_pages)
#         return render(request, 'events.html', {'events': final_events,
#                                                'pagination': gen_page_list(page, p.num_pages)})
#
#     def post(self,request):
#         form = CreateNewEvent(request.POST)
#         if form.is_valid():
#             event = form.save(commit=False)
#             event.creator = request.user
#             event.date = timezone.now()
#             event.save()
#             return redirect('single_event_page', event_id=event.pk)
#         return render(request, 'add-event.html', {'form': form})
