from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from eventsSite.forms import
from eventsSite.models import EventsList


# Create your views here.

@login_required
def create_event(request):
    """
    Страница создания мероприятия

    :param request: объект с деталями запроса
    :type request: :class: 'django.http.HttpRequest'
    :return: html страница
    """

    form = SplitForm(request.POST)
    context = {'form': form}

    user = request.user

    if user.is_authenticated:
        record = EventsList(
            name="default"
        stages = "default"
        date = "default"
        info = "default"
        )
        record.save()

    return render(request, 'create_event.html', context)
