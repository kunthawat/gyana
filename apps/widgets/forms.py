from apps.dataflows.models import Node
from apps.datasets.models import Dataset
from django import forms
from django.forms.widgets import HiddenInput

from .models import Widget


class WidgetForm(forms.ModelForm):
    class Meta:
        model = Widget
        fields = ["name", "dashboard"]
        widgets = {"dashboard": HiddenInput()}

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)
        if project:
            source_type = "dataset" if self.instance.dataset else "node"
            self.fields["source"] = forms.ChoiceField(
                initial=f"{source_type}_{getattr(self.instance, source_type).id}",
                choices=[
                    *[
                        (f"dataset_{d.id}", d.name)
                        for d in Dataset.objects.filter(project=project)
                    ],
                    *[
                        (f"node_{n.id}", n.output_name)
                        for n in Node.objects.filter(
                            dataflow__project=project, kind=Node.Kind.OUTPUT
                        )
                    ],
                ],
            )


class WidgetConfigForm(forms.ModelForm):
    class Meta:
        model = Widget
        fields = ["kind", "label", "value"]

    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/a/30766247/15425660
        self.columns = kwargs.pop("columns")
        super().__init__(*args, **kwargs)
        self.fields["label"].choices = self.columns
        self.fields["value"].choices = self.columns

    label = forms.ChoiceField(choices=())
    value = forms.ChoiceField(choices=())
