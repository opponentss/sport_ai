"""
健身指南模块表单定义

本模块定义了健身指南模块使用的表单类，用于处理器材、饮食建议和肌肉认识的添加和编辑。
表单提供了友好的输入界面和客户端验证。

主要表单：
- EquipmentForm: 器材信息表单
- DietItemForm: 饮食建议表单
- MuscleGroupForm: 肌肉群表单
- MuscleItemForm: 肌肉部位表单
"""

from django import forms
from .models import Equipment, DietItem, MuscleGroup, MuscleItem


class EquipmentForm(forms.ModelForm):
    """器材表单"""

    class Meta:
        model = Equipment
        fields = ['name', 'category', 'image', 'video_url', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入器材名称'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/watch?v=...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '请输入器材的详细描述和使用方法'
            }),
        }

    def clean_video_url(self):
        video_url = self.cleaned_data.get('video_url')
        if video_url:
            video_url = video_url.strip()
        return video_url


class DietItemForm(forms.ModelForm):
    """饮食建议表单"""

    class Meta:
        model = DietItem
        fields = ['title', 'category', 'image', 'video_url', 'content', 'is_featured']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入饮食建议标题'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/watch?v=...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': '请输入饮食建议的详细内容...'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_video_url(self):
        video_url = self.cleaned_data.get('video_url')
        if video_url:
            video_url = video_url.strip()
        return video_url


class MuscleGroupForm(forms.ModelForm):
    """
    肌肉群表单

    用于创建和编辑肌肉群分类信息。
    """

    class Meta:
        model = MuscleGroup
        fields = ['name', 'latin_name', 'category', 'icon', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入肌肉群名称，如：胸部、背部'
            }),
            'latin_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '如：Pectoralis、Latissimus'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '输入emoji图标，如：💪'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '简要描述该肌肉群的位置和功能'
            }),
        }


class MuscleItemForm(forms.ModelForm):
    """
    肌肉部位表单

    用于创建和编辑肌肉部位的详细信息，包含肌肉图片、视频链接、描述和训练要点。
    """

    class Meta:
        model = MuscleItem
        fields = ['muscle_group', 'name', 'latin_name', 'image', 'video_url', 'description', 'training_tips', 'is_featured']

        widgets = {
            'muscle_group': forms.Select(attrs={
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入肌肉部位名称，如：胸大肌'
            }),
            'latin_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '如：Pectoralis Major'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/watch?v=...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '详细描述该肌肉的位置、功能和训练方法'
            }),
            'training_tips': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '输入该肌肉的训练要点和注意事项'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_video_url(self):
        video_url = self.cleaned_data.get('video_url')
        if video_url:
            video_url = video_url.strip()
        return video_url