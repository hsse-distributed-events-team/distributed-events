from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from eventsSite.forms import Event
from eventsSite.models import EventData


# Create your views here.

@login_required
def create_event(request):
    """
    Страница создания мероприятия

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """

    form = Event(request.POST)
    context = {'form': form}

    if form.is_valid():
        date = form.cleaned_data['date']

        user = request.user

        if user.is_authenticated:
            record = EventData()
            record.save()

    return render(request, 'create_event.html', context)
