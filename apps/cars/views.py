from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics, viewsets

from .models import Car, CarModel
from .forms import CarForm
from .permissions import CarPermission, CarModelPermission
from .serializers import CarSerializer, CarModelSerializer


class CarModelAPIViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all().order_by('-pk')
    serializer_class = CarModelSerializer
    permission_classes = [CarModelPermission]


class CarAPICreateView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [CarPermission]

    def perform_create(self, serializer):
        serializer.save(racer=self.request.user)


class CarAPIRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [CarPermission]


class CarCreateView(generic.CreateView):
    form_class = CarForm
    template_name = 'cars/object_create_base.html'

    def form_valid(self, form):
        form.instance.racer = self.request.user
        messages.success(self.request, f'Car has been applied.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Car'

        return context

    def get_success_url(self):
        return self.object.get_absolute_url()


class CarDetailView(generic.DetailView):
    model = Car
    context_object_name = 'car'
    template_name = 'cars/car_detail.html'

    def get_queryset(self):
        qs = super().get_queryset().select_related('car_model', 'racer')
        return qs


class CarUpdateView(generic.UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'cars/car_update.html'

    def get_object(self, queryset=None):
        song_object = super().get_queryset().select_related('car_model').get(racer=self.request.user)

        return song_object

    def form_valid(self, form):
        messages.success(self.request, f'Song has been updated.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class CarDeleteView(generic.DeleteView):
    model = Car
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, f'Car has been successfully deleted.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)
