from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    COACH_CHOICES = [
        ('calm', '冷静型'),
        ('rational', '理性型'),
        ('light_tsukkomi', '轻吐槽型'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    anonymous_mode = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=True)
    low_social_mode = models.BooleanField(default=False)
    preferred_coach_type = models.CharField(max_length=20, choices=COACH_CHOICES, default='calm')
    do_not_disturb = models.BooleanField(default=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    streak_days = models.IntegerField(default=0)
    last_training_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_xp(self, amount):
        self.xp += amount
        new_level = self.xp // 100 + 1
        leveled_up = new_level > self.level
        self.level = new_level
        self.save()
        return leveled_up

    def __str__(self):
        display = '匿名用户' if self.anonymous_mode else self.user.username
        return f'{display} Lv.{self.level}'


class TrainingPlan(models.Model):
    MOOD_TAGS = [
        ('anxious', '焦虑舒缓'),
        ('low_energy', '低能量唤醒'),
        ('normal', '日常保持'),
        ('night', '夜间放松'),
    ]

    SPACE_TAGS = [
        ('dorm', '宿舍模式'),
        ('room', '房间模式'),
        ('any', '任意空间'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_minutes = models.IntegerField()
    mood_tag = models.CharField(max_length=20, choices=MOOD_TAGS, default='normal')
    space_tag = models.CharField(max_length=20, choices=SPACE_TAGS, default='any')
    silent_mode = models.BooleanField(default=True)
    icon = models.CharField(max_length=50, default='🏠')
    xp_reward = models.IntegerField(default=30)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'duration_minutes']

    def __str__(self):
        return f'{self.name} ({self.duration_minutes}分钟)'


class TrainingExercise(models.Model):
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_seconds = models.IntegerField(help_text='单个动作时长（秒）')
    voice_guide = models.TextField(help_text='语音引导文案', blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} ({self.duration_seconds}秒)'


class TrainingSession(models.Model):
    STATUS_CHOICES = [
        ('completed', '已完成'),
        ('partial', '部分完成'),
        ('skipped', '已跳过'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_sessions')
    plan = models.ForeignKey(TrainingPlan, on_delete=models.SET_NULL, null=True, related_name='sessions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    xp_earned = models.IntegerField(default=0)
    exercises_completed = models.IntegerField(default=0)
    exercises_total = models.IntegerField(default=0)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.plan.name if self.plan else "自由训练"} - {self.get_status_display()}'


class Achievement(models.Model):
    CONDITION_TYPES = [
        ('total_sessions', '累计训练次数'),
        ('streak_days', '连续训练天数'),
        ('total_xp', '累计经验值'),
        ('first_session', '首次训练'),
        ('plan_master', '完成所有训练方案'),
        ('night_owl', '深夜训练'),
        ('gentle_soul', '完成舒缓训练'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    condition_type = models.CharField(max_length=30, choices=CONDITION_TYPES)
    condition_value = models.IntegerField(default=1)
    xp_reward = models.IntegerField(default=50)
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'achievement']

    def __str__(self):
        return f'{self.user.username} - {self.achievement.name}'
