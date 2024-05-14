from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from .models import Racer


class RacerCreateForm(UserCreationForm):
    year_of_birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=True)

    class Meta:
        model = Racer
        fields = ["username", 'number', 'first_name', 'second_name', 'description', "password1", "password2",
                  'country', 'year_of_birth', 'stance']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes ':' as label suffix

        self.fields['username'].help_text = 'Letters, numbers and @/./+/-/_ only.'
        self.fields['password1'].help_text = '8-20 characters, letters and numbers, no spaces.'
        self.fields['password2'].help_text = None

        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'{field.label}*'
            else:
                field.label = f'{field.label} (optional)'

    def save(self, commit=True):
        racer = super().save(commit=False)
        racer.number = self.cleaned_data['number']
        racer.first_name = self.cleaned_data['first_name']
        racer.second_name = self.cleaned_data['second_name']
        racer.year_of_birth = self.cleaned_data['year_of_birth']
        racer.stance = self.cleaned_data['stance']
        if commit:
            racer.save()
        return racer


class RacerUpdateForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ["username", 'number', 'first_name', 'second_name', 'description', 'country', 'year_of_birth',
                  'stance']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes ':' as label suffix
