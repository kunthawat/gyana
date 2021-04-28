from django import forms

from .models import Dataflow


class DataflowForm(forms.ModelForm):
    class Meta:
        model = Dataflow
        fields = ["name"]


class PivotNode(forms.Form):
    index = forms.CharField()
    columns = forms.CharField()
    values = forms.CharField()


class UnpivotNode(forms.Form):
    id_vars = forms.CharField()
    value_vars = forms.CharField()


KIND_TO_FORM = {"pivot": PivotNode, "unpivot": UnpivotNode}
