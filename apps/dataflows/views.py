from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView
from turbo_response.views import TurboCreateView, TurboUpdateView

from .forms import DataflowForm
from .models import Dataflow


class DataflowList(ListView):
    template_name = "dataflows/list.html"
    model = Dataflow
    paginate_by = 20


class DataflowCreate(TurboCreateView):
    template_name = "dataflows/create.html"
    model = Dataflow
    form_class = DataflowForm
    success_url = reverse_lazy('dataflows:list')


class DataflowDetail(DetailView):
    template_name = "dataflows/detail.html"
    model = Dataflow


class DataflowUpdate(TurboUpdateView):
    template_name = "dataflows/update.html"
    model = Dataflow
    form_class = DataflowForm
    success_url = reverse_lazy('dataflows:list')


class DataflowDelete(DeleteView):
    template_name = "dataflows/delete.html"
    model = Dataflow
    success_url = reverse_lazy('dataflows:list')
