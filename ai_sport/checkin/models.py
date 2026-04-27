from django.db import models
from django.contrib.auth.models import User


class ExerciseType(models.Model):
    CATEGORIES = (
        ('home', '🏠 居家训练'),
        ('outdoor', '🏃 户外运动'),
        ('gym', '🏋️ 器械训练'),
        ('cardio', '❤️ 有氧燃脂'),
        ('stretch', '🧘 拉伸放松'),
    )

    DIFFICULTY = (
        ('beginner', '入门'),
        ('intermediate', '进阶'),
        ('challenge', '挑战'),
    )

    name = models.CharField(max_length=100, verbose_name='运动名称')
    category = models.CharField(max_length=20, choices=CATEGORIES, verbose_name='运动类别')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY, default='beginner', verbose_name='难度')
    calories_per_minute = models.FloatField(default=5.0, verbose_name='每分钟消耗卡路里')
    icon = models.CharField(max_length=50, default='💪', verbose_name='图标')
    strength_gain = models.IntegerField(default=1, verbose_name='力量增长')
    endurance_gain = models.IntegerField(default=1, verbose_name='耐力增长')
    agility_gain = models.IntegerField(default=0, verbose_name='敏捷增长')
    is_active = models.BooleanField(default=True, verbose_name='启用')

    class Meta:
        verbose_name = '运动类型'
        verbose_name_plural = '运动类型列表'
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.icon} {self.name}'


class Checkin(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='checkins'
    )

    exercise_type = models.ForeignKey(
        ExerciseType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='运动类型',
        related_name='checkins'
    )

    activity = models.CharField(
        max_length=100,
        verbose_name='活动名称',
        help_text='输入运动项目名称，如"跑步"、"游泳"、"健身"等'
    )

    duration = models.IntegerField(
        verbose_name='活动时长（分钟）',
        help_text='输入活动持续时间，单位为分钟'
    )

    calories_burned = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='消耗卡路里',
        help_text='该次运动消耗的卡路里（自动计算或手动输入）'
    )

    date = models.DateField(
        auto_now_add=True,
        verbose_name='打卡日期'
    )

    time = models.TimeField(
        auto_now_add=True,
        verbose_name='打卡时间'
    )

    latitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='纬度',
        help_text='GPS纬度坐标，可通过地图获取'
    )

    longitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='经度',
        help_text='GPS经度坐标，可通过地图获取'
    )

    location = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='位置描述',
        help_text='输入位置名称，如"XX健身房"、"XX公园"'
    )

    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='备注',
        help_text='添加任何其他想记录的信息'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    class Meta:
        verbose_name = '运动打卡'
        verbose_name_plural = '运动打卡记录'
        ordering = ['-date', '-time']

    def __str__(self):
        return f'{self.user.username} - {self.activity} - {self.date}'
