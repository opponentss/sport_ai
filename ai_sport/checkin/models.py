from django.db import models
from django.contrib.auth.models import User

class Checkin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=100)
    duration = models.IntegerField(help_text='活动时长（分钟）')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    # 定位功能
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.activity} - {self.date}'
