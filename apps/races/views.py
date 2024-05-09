from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect
from django.utils import timezone
from django.views import generic
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Race, RaceEntry
from .serializers import RaceSerializer
from .permissions import RacePermission, IsStaffUser

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


@api_view(['POST'])
@permission_classes([IsStaffUser])
def complete_race(request, pk):
    if request.method == 'POST':
        race_obj = Race.objects.prefetch_related('racers').get(pk=pk)
        racers = race_obj.racers.all().order_by('car__car_model__speed')
        if racers.count() == race_obj.race_limit and race_obj.completion_date is None:
            race_entry = RaceEntry.objects.all()
            racers_ids = [racer.id for racer in racers]
            for position, racer_id in enumerate(racers_ids, start=1):
                racer_entry = race_entry.get(race=race_obj, racer_id=racer_id)
                racer_entry.position = position
                racer_entry.save()
            for racer in racers:
                racer_entry = race_entry.select_related('racer').filter(racer=racer)
                race_entry_obj = racer_entry.get(race=race_obj)
                race_entry_obj.racer.score = (race_obj.race_limit - race_entry_obj.position + 1) / racer_entry.count()
                race_entry_obj.racer.save()
            race_obj.completion_date = timezone.now()
            race_obj.save()
        return Response({'message': 'Race was completed.'})


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
    racers_count = racers.count()

    if racers_count < race.race_limit:
        if request.user.number not in numbers_of_racers:
            if request.user.first_name and request.user.second_name:
                if request.user.car.exists():
                    race.racers.add(request.user)
                    messages.success(request, f'Successfully applied for {race.name} race!')
                else:
                    messages.error(request, 'You dont have a car.')
            else:
                messages.error(request, 'You dont have a first/last name.')
        else:
            messages.error(request, 'Racer with this number already applied. Change your number.')
    else:
        messages.error(request, 'This race is packed.')

    return redirect(request.META.get('HTTP_REFERER'))


def cancel_application_for_race(request, pk):
    race = Race.objects.get(pk=pk)
    racers = race.racers

    if request.user in racers.all() and not race.completion_date:
        racers.remove(request.user)
        messages.success(request, f'Successfully cancelled application for {race.name} race')

    return redirect(request.META.get('HTTP_REFERER'))


