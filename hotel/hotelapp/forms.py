from django import forms

from  .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'extr_id',
            'name',
            'city',
        )
        widgets = {
            'name' : forms.TextInput,
            'city' : forms.TextInput,
        }