from .models import ProgressStatus
from django import forms

class ProgressStatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["target_value"].widget.attrs.update({"class": "form-control"})
        self.fields["info"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = ProgressStatus
        fields = ('target_value', 'info')