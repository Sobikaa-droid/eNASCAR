from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Racer


class RacerCreateForm(UserCreationForm):
    number = forms.IntegerField(required=True, min_value=1, max_value=99)
    first_name = forms.CharField(required=True, max_length=100)
    second_name = forms.CharField(required=True, max_length=100)

    class Meta:
        model = Racer
        fields = ["username", 'description', "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes ':' as label suffix

        self.fields['username'].help_text = 'Letters, numbers and @/./+/-/_ only.'
        self.fields['password1'].help_text = '8-20 characters, letters and numbers, no spaces.'
        self.fields['password2'].help_text = None

    def save(self, commit=True):
        racer = super().save(commit=False)
        racer.number = self.cleaned_data['number']
        racer.first_name = self.cleaned_data['first_name']
        racer.second_name = self.cleaned_data['second_name']
        if commit:
            racer.save()
        return racer


# class RacerUpdateForm(forms.ModelForm):
#     number = forms.IntegerField(required=True, min_value=1, max_value=99)
#     first_name = forms.CharField(required=True, max_length=100)
#     second_name = forms.CharField(required=True, max_length=100)
#
#     class Meta:
#         model = Racer
#         fields = ["username", 'description', "password1", "password2"]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.car_formset = RacerCarFormSet(instance=self.instance)
#         self.label_suffix = ""  # Removes ':' as label suffix
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.label_suffix = ""  # Removes ':' as label suffix
