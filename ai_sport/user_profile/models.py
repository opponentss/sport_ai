from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    用户扩展模型 - 存储头像等额外信息
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='头像', blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} 的个人信息'
    
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
