from django import forms

from .models import Dataflow


class DataflowForm(forms.ModelForm):
    class Meta:
        model = Dataflow
        fields = ['name']
