from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Prefetch, Case, When, Value, CharField, IntegerField
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views import generic
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
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        race = get_object_or_404(Race.objects.prefetch_related('racers').all(), pk=pk, completion_date__isnull=True)
        user = request.user

        # Check if the user has an active application for another race
        if user.race_set.filter(pk=pk).exists():
            return Response(
                {'error': f'You are already applied for this race.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the race is full
        if race.racers.count() >= race.race_limit:
            return Response(
                {'error': 'This race is packed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if racer has a car
        try:
            user.car
        except user._meta.model.car.RelatedObjectDoesNotExist:
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
        with transaction.atomic():
            race.racers.add(user)
            race_entry_qs = RaceEntry.objects.filter(race=race)
            taken_positions = [i.position for i in race_entry_qs]
            race_entry = get_object_or_404(race_entry_qs, racer=user)
            available_positions = [i for i in range(1, race.race_limit + 1) if i not in taken_positions]
            race_entry.position = available_positions[0]
            race_entry.save()
            return Response(
                {'success': f'Successfully applied for {race.name} race!'},
                status=status.HTTP_200_OK
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

        race.racers.remove(user)
        return Response(
            {'success': f'Successfully cancelled application for {race.name} race'},
            status=status.HTTP_200_OK
        )


class CompleteRaceAPIView(APIView):
    permission_classes = [IsStaffUser]

    def post(self, request, pk):
        race = get_object_or_404(Race.objects.prefetch_related('racers'), pk=pk, completion_date__isnull=True)
        racers = race.racers.all().order_by('car__car_model__speed')

        if racers.count() != race.race_limit:
            return Response(
                {'error': 'Not enough racers to complete race.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            race_entries = RaceEntry.objects.select_related('racer').filter(race=race, racer__in=racers)
            for place, race_entry in enumerate(race_entries, start=1):
                race_entry.place = place
                race_entry.save()
            for race_entry in race_entries:
                new_score = race_entry.racer.score + (race.race_limit - race_entry.place + 1) / race_entries.count()
                race_entry.racer.score = new_score
                race_entry.racer.save()

            race.completion_date = timezone.now()
            race.save()
            return Response(
                {'success': f'{race.name} was successfully completed.'},
                status=status.HTTP_200_OK
            )


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


class RaceEntryOfRaceListView(generic.ListView):
    model = RaceEntry
    context_object_name = 'race_entry'
    template_name = 'races/race_entry_of_race_list.html'

    def get_queryset(self):
        qs = super().get_queryset().select_related('racer').filter(race__pk=self.kwargs.get('pk'))
        obj = qs.first()
        if obj and obj.place:
            order_field = 'place'
        else:
            order_field = 'position'
        return qs.order_by(order_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['race'] = get_object_or_404(Race, pk=self.kwargs.get('pk'))

        return context


def apply_for_race(request, pk):
    if request.method == 'POST':
        race = get_object_or_404(Race.objects.prefetch_related('racers').all(), pk=pk, completion_date__isnull=True)
        user = request.user

        # Check if the user has an active application for another race
        if user.race_set.filter(pk=pk).exists():
            messages.error(request, f'You are already applied for this race.')
            return redirect('races:race_detail', pk=pk)

        # Check if the race is full
        if race.racers.count() >= race.race_limit:
            messages.error(request, 'This race is packed.')
            return redirect('races:race_detail', pk=pk)

        # Check if racer has a car
        try:
            user.car
        except user._meta.model.car.RelatedObjectDoesNotExist:
            messages.error(request, 'You don\'t have a car.')
            return redirect('races:race_detail', pk=pk)

        # Check if racer's number is unique in the race
        if race.racers.filter(number=user.number).exists():
            messages.error(request, 'Racer with this number already applied. Change your number.')
            return redirect('races:race_detail', pk=pk)

        # Add the user to the race and set him an available position
        with transaction.atomic():
            race.racers.add(user)
            race_entry_qs = RaceEntry.objects.filter(race=race)
            taken_positions = [i.position for i in race_entry_qs]
            race_entry = get_object_or_404(race_entry_qs, racer=user)
            available_positions = [i for i in range(1, race.race_limit + 1) if i not in taken_positions]
            race_entry.position = available_positions[0]
            race_entry.save()
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

        race.racers.remove(user)
        messages.success(request, f'Successfully cancelled application for {race.name} race')
        return redirect('races:race_detail', pk=pk)
    else:
        messages.warning(request, f'Method {request.method} is not allowed.')
        return redirect('races:race_detail', pk=pk)
