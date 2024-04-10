from django.db.models import Count
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
    queryset = Race.objects.all()
    serializer_class = RaceSerializer
    permission_classes = [RacePermission]
    pagination_class = ListPagination


class RaceListView(generic.ListView):
    model = Race
    context_object_name = 'races'
    paginate_by = 15
    template_name = "races/races_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(racers_count=Count('racers'))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class RaceDetailView(generic.DetailView):
    model = Race
    context_object_name = 'race'
    template_name = 'races/race_detail.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        race_object = Race.objects.prefetch_related('racers').get(pk=pk)

        return race_object

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     pk = self.kwargs.get('pk')
    #     obj = self.get_queryset().filter(pk=pk)
    #     context['racers_count'] = obj.racers_set.count()
    #
    #     return context


# class AddRacerToRaceView(generics.UpdateAPIView):
#     serializer_class = RaceSerializer
#     queryset = Race.objects.all()
#
#     def update(self, request, *args, **kwargs):
#         race = self.get_object()
#         racers_numbers = race.racers.values_list('number', flat=True)
#         racer = request.user
#         # if not racer.number:
#         #     raise ValueError('You dont have a number')
#         if not racer.car:
#             raise ValueError('You dont have a car')
#         if racer.number in racers_numbers:
#             raise ValueError(f'The number {racer.number} is already registered to this race. Change your number.')
#
#         race.racers.add(request.user)
#         race.save()
#
#         serializer = self.get_serializer(race)
#         return Response(serializer.data)
