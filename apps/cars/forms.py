from django import forms

from .models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_model', 'color']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes ':' as label suffix
