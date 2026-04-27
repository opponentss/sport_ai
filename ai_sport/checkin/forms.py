from django import forms
from .models import Checkin, ExerciseType


class CheckinForm(forms.ModelForm):
    class Meta:
        model = Checkin
        fields = ['exercise_type', 'activity', 'duration', 'calories_burned', 'latitude', 'longitude', 'location', 'notes']
        widgets = {
            'exercise_type': forms.Select(attrs={'class': 'form-control'}),
            'activity': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    exercise_type = forms.ModelChoiceField(
        queryset=ExerciseType.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='运动类型'
    )
