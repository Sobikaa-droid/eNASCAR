from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from rest_framework import generics
from rest_framework.response import Response

from .models import Race
from .serializers import RaceSerializer
from .permissions import RacePermission

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination


# pagination class
class ListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class RaceAPIViewSet(viewsets.ModelViewSet):
    queryset = Race.objects.all().order_by('-pk')
    serializer_class = RaceSerializer
    permission_classes = [RacePermission]
    pagination_class = ListPagination


class RaceListView(generic.ListView):
    model = Race
    context_object_name = 'races'
    paginate_by = 15
    template_name = "races/races_list.html"

    def get_queryset(self):
        return super().get_queryset().order_by('-pk').annotate(racers_count=Count('racers'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class RaceDetailView(generic.DetailView):
    model = Race
    context_object_name = 'race'
    template_name = 'races/race_detail.html'


class RaceRacersListView(generic.DetailView):
    model = Race
    context_object_name = 'race'
    template_name = 'races/race_racers_list.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('racers')

    # def get_object(self, queryset=None):
    #     pk = self.kwargs.get('pk')
    #     race_object = Race.objects.prefetch_related('racers').get(pk=pk)
    #
    #     return race_object


def apply_for_race(request, pk):
    race = Race.objects.get(pk=pk)
    racers = race.racers.all()
    numbers_of_racers = racers.values_list('number', flat=True)

    if racers.count() < race.race_limit:
        if request.user.number not in numbers_of_racers:
            if request.user.first_name and request.user.second_name:
                if request.user.car:
                    race.racers.add(request.user)
                    messages.success(request, f'Successfully applied for {race.name} race!')
                    Race.objects.complete_race(pk=pk)
                else:
                    messages.error(request, 'You dont have a car.')
            else:
                messages.error(request, 'You dont have a first/last name.')
        else:
            messages.error(request, 'Racer with this number already applied. Change your number.')
    else:
        messages.error(request, 'This race is packed.')

    return redirect(request.META.get('HTTP_REFERER'))


