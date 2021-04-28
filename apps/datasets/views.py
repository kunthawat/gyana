from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView
from turbo_response.views import TurboCreateView, TurboUpdateView

from .forms import DatasetForm
from .models import Dataset


class DatasetList(ListView):
    template_name = "datasets/list.html"
    model = Dataset
    paginate_by = 20


class DatasetCreate(TurboCreateView):
    template_name = "datasets/create.html"
    model = Dataset
    form_class = DatasetForm
    success_url = reverse_lazy('datasets:list')


class DatasetDetail(DetailView):
    template_name = "datasets/detail.html"
    model = Dataset


class DatasetUpdate(TurboUpdateView):
    template_name = "datasets/update.html"
    model = Dataset
    form_class = DatasetForm
    success_url = reverse_lazy('datasets:list')


class DatasetDelete(DeleteView):
    template_name = "datasets/delete.html"
    model = Dataset
    success_url = reverse_lazy('datasets:list')
