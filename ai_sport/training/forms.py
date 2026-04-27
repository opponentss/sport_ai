from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': '取一个只有你知道的名字'})
        self.fields['username'].label = '用户名'
        self.fields['password1'].label = '密码'
        self.fields['password1'].widget.attrs.update({'placeholder': '至少8位'})
        self.fields['password2'].label = '确认密码'
        self.fields['password2'].widget.attrs.update({'placeholder': '再输一次'})


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['anonymous_mode', 'dark_mode', 'low_social_mode', 'preferred_coach_type', 'do_not_disturb']
        widgets = {
            'preferred_coach_type': forms.RadioSelect,
        }
