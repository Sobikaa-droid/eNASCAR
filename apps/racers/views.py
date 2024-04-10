from django.views import generic
from rest_framework import generics, viewsets, mixins, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Racer
from .serializers import RacerSerializer
from .permissions import RacerPermission


# pagination class
class ListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class RacerAPIViewSet(viewsets.ModelViewSet):
    queryset = Racer.objects.all()
    serializer_class = RacerSerializer
    permission_classes = [RacerPermission]
    pagination_class = ListPagination


class RacerListView(generic.ListView):
    context_object_name = 'racers'
    paginate_by = 15
    template_name = "racers/racers_list.html"

    def get_queryset(self):
        return Racer.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['racers_count'] = self.get_queryset().distinct().count()

        return context


class RacerDetailView(generic.DetailView):
    model = Racer
    context_object_name = 'racer'
    template_name = 'racers/racer_detail.html'
