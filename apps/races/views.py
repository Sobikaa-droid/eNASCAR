from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views import generic
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Race, RaceEntry
from .serializers import RaceSerializer
from .permissions import IsStaffUserOrReadOnly, IsStaffUser

from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination


# pagination class
class ListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class RaceAPIViewSet(viewsets.ModelViewSet):
    queryset = Race.objects.all().order_by('-pk')
    serializer_class = RaceSerializer
    permission_classes = [IsStaffUserOrReadOnly]
    pagination_class = ListPagination


class ApplyForRaceAPIView(APIView):
    def post(self, request, pk):
        race = get_object_or_404(Race, pk=pk, completion_date__isnull=True)
        user = request.user

        # Check if the user has an active application for another race
        active_application = user.race_set.filter(completion_date__isnull=True)
        if active_application.exists():
            applied_race = active_application.first()
            return Response(
                {'error': f'You are already applied for {applied_race.name} race.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the race is full
        if race.racers.count() >= race.race_limit:
            return Response(
                {'error': 'This race is packed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if racer has a car
        if not user.car:
            return Response(
                {'error': 'You dont have a car.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if racer's number is unique in the race
        if race.racers.filter(number=user.number).exists():
            return Response(
                {'error': 'Racer with this number already applied. Change your number.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add the user to the race
        try:
            race.racers.add(user)
            return Response(
                {'success': f'Successfully applied for {race.name} race!'},
                status=status.HTTP_200_OK
            )
        except ValueError as error:
            return Response(
                {'error': error},
                status=status.HTTP_400_BAD_REQUEST
            )


class CancelApplicationForRaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        race = get_object_or_404(Race, pk=pk, completion_date__isnull=True)
        user = request.user

        # Check if racer's not applied for the race
        if not race.racers.filter(pk=user.pk).exists():
            return Response(
                {'error': 'You are not applied for this race'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if race is not completed
        if race.completion_date:
            return Response(
                {'error': 'This race is over'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            race.racers.remove(user)
            return Response(
                {'success': f'Successfully cancelled application for {race.name} race'},
                status=status.HTTP_200_OK
            )
        except ValueError as error:
            return Response(
                {'error': error},
                status=status.HTTP_400_BAD_REQUEST
            )


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
    template_name = "races/races_list_base.html"

    def get_queryset(self):
        return super().get_queryset().filter(completion_date__isnull=True).order_by('-pk').annotate(
            racers_count=Count('racers'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Active'

        return context


class CompletedRaceListView(generic.ListView):
    model = Race
    context_object_name = 'races'
    paginate_by = 15
    template_name = "races/races_list_base.html"

    def get_queryset(self):
        return super().get_queryset().filter(completion_date__isnull=False).order_by('-pk').annotate(
            racers_count=Count('racers'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Completed'

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


def apply_for_race(request, pk):
    if request.method == 'POST':
        race = get_object_or_404(Race, pk=pk, completion_date__isnull=True)
        user = request.user

        # Check if the user has an active application for another race
        active_application = user.race_set.filter(completion_date__isnull=True)
        if active_application.exists():
            applied_race = active_application.first()
            messages.error(request, f'You are already applied for {applied_race.name} race.')
            return redirect('races:race_detail', pk=pk)

        # Check if the race is full
        if race.racers.count() >= race.race_limit:
            messages.error(request, 'This race is packed.')
            return redirect('races:race_detail', pk=pk)

        # Check if racer has a car
        if not user.car:
            messages.error(request, 'You don\'t have a car.')
            return redirect('races:race_detail', pk=pk)

        # Check if racer's number is unique in the race
        if race.racers.filter(number=user.number).exists():
            messages.error(request, 'Racer with this number already applied. Change your number.')
            return redirect('races:race_detail', pk=pk)

        # Add the user to the race
        race.racers.add(user)
        messages.success(request, f'Successfully applied for {race.name} race!')
        return redirect('races:race_detail', pk=pk)
    else:
        messages.warning(request, f'Method {request.method} is not allowed.')
        return redirect('races:race_detail', pk=pk)


def cancel_application_for_race(request, pk):
    if request.method == 'POST':
        race = get_object_or_404(Race, pk=pk, completion_date__isnull=True)
        user = request.user

        # Check if racer's not applied for the race
        if not race.racers.filter(pk=user.pk).exists():
            messages.error(request, f'You are not applied for this race')
            return redirect('races:race_detail', pk=pk)

        # Check if race is over
        if race.completion_date:
            messages.error(request, f'This race is over')
            return redirect('races:race_detail', pk=pk)

        try:
            race.racers.remove(user)
            messages.success(request, f'Successfully cancelled application for {race.name} race')
        except ValueError:
            messages.error(request, f'An error occurred while canceling your application')

        return redirect('races:race_detail', pk=pk)
    else:
        messages.warning(request, f'Method {request.method} is not allowed.')
        return redirect('races:race_detail', pk=pk)
