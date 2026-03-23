from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SleepRecord(models.Model):
    SLEEP_QUALITY = (
        ('excellent', '优秀'),
        ('good', '良好'),
        ('fair', '一般'),
        ('poor', '较差'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    sleep_time = models.TimeField(help_text='入睡时间')
    wake_time = models.TimeField(help_text='起床时间')
    quality = models.CharField(max_length=20, choices=SLEEP_QUALITY, default='fair')
    duration = models.FloatField(help_text='睡眠时长（小时）', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.quality}'
