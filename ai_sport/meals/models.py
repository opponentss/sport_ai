from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Meal(models.Model):
    MEAL_TYPES = (
        ('breakfast', '早餐'),
        ('lunch', '午餐'),
        ('dinner', '晚餐'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    # 拍照功能
    image = models.ImageField(upload_to='meal_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    calories = models.IntegerField(null=True, blank=True, help_text='卡路里')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.get_meal_type_display()} - {self.date}'
