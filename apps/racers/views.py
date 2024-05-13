from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Racer
from .serializers import RacerSerializer
from .permissions import RacerPermission
from .forms import RacerCreateForm, RacerUpdateForm
from apps.races.models import Race


# pagination class
class ListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class RacerAPIViewSet(viewsets.ModelViewSet):
    queryset = Racer.objects.filter(is_staff=False).order_by('-pk')
    serializer_class = RacerSerializer
    permission_classes = [RacerPermission]
    pagination_class = ListPagination


class RacerListView(generic.ListView):
    model = Racer
    context_object_name = 'racers'
    paginate_by = 15
    template_name = "racers/racers_list.html"

    def get_queryset(self):
        qs = super().get_queryset().filter(is_staff=False).order_by('-pk')

        search_val = self.request.GET.get('search_val', None)
        order_val = self.request.GET.get('order_by', '-pk')
        if search_val:
            qs = qs.filter(username__icontains=search_val)
        qs = qs.order_by(order_val)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['racers_count'] = self.get_queryset().distinct().count()

        return context


class RacerDetailView(generic.DetailView):
    model = Racer
    context_object_name = 'racer'
    template_name = 'racers/racer_detail.html'

    def get_queryset(self):
        prefetch_racers = Prefetch('race_set', queryset=Race.objects.prefetch_related('racers'))
        qs = super().get_queryset().select_related('car').prefetch_related(prefetch_racers).filter(is_staff=False)
        return qs


class RacerUpdateView(generic.UpdateView):
    model = Racer
    form_class = RacerUpdateForm
    template_name = 'racers/racer_update.html'

    def get_object(self, queryset=None):
        racer = super().get_queryset().get(pk=self.request.user.pk)

        return racer

    def form_valid(self, form):
        messages.success(self.request, f'Profile has been updated.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class RacerRegisterView(generic.FormView):
    form_class = RacerCreateForm
    success_url = reverse_lazy('home')
    template_name = 'racers/register.html'

    def form_valid(self, form):
        form.save()
        new_user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        login(self.request, new_user)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)


class RacerLoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    template_name = 'racers/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)


class RacerLogoutView(LogoutView):
    next_page = reverse_lazy('home')
