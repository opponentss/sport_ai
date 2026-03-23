from django import forms
from .models import Checkin

class CheckinForm(forms.ModelForm):
    class Meta:
        model = Checkin
        fields = ['activity', 'duration', 'latitude', 'longitude', 'location', 'notes']
        widgets = {
            'activity': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
