from django import forms
from .models import SleepRecord

class SleepRecordForm(forms.ModelForm):
    class Meta:
        model = SleepRecord
        fields = ['date', 'sleep_time', 'wake_time', 'quality', 'duration', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sleep_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'wake_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'quality': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
