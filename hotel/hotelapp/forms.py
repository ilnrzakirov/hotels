from django import forms

from  .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'extr_id',
            'name',
            'city',
            'city_id',
        )
        widgets = {
            'name' : forms.TextInput,
            'city' : forms.TextInput,
        }