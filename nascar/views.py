from django.shortcuts import render

from apps.racers.models import Racer
from apps.races.models import Race


def home(request):
    context = {
        'active_races': Race.objects.filter(completion_date__isnull=True),
        'completed_races': Race.objects.filter(completion_date__isnull=False),
        'racers': Racer.objects.filter(is_staff=False),
    }
    return render(request, 'home.html', context)
