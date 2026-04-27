from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


XP_PER_LEVEL = 100


class UserGameProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='game_profile'
    )

    xp = models.IntegerField(default=0, verbose_name='经验值')
    level = models.IntegerField(default=1, verbose_name='等级')

    strength = models.IntegerField(default=1, verbose_name='力量')
    endurance = models.IntegerField(default=1, verbose_name='耐力')
    agility = models.IntegerField(default=1, verbose_name='敏捷')
    willpower = models.IntegerField(default=1, verbose_name='意志')

    total_checkins = models.IntegerField(default=0, verbose_name='总打卡次数')
    total_exercise_minutes = models.IntegerField(default=0, verbose_name='总运动时长(分钟)')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户游戏档案'
        verbose_name_plural = '用户游戏档案列表'

    def __str__(self):
        return f'{self.user.username} - Lv.{self.level}'

    @property
    def xp_to_next_level(self):
        current_level_xp = (self.level - 1) * XP_PER_LEVEL
        xp_in_level = self.xp - current_level_xp
        return XP_PER_LEVEL

    @property
    def xp_current_level(self):
        current_level_xp = (self.level - 1) * XP_PER_LEVEL
        return self.xp - current_level_xp

    @property
    def xp_remaining(self):
        current_level_xp = (self.level - 1) * XP_PER_LEVEL
        xp_in_level = self.xp - current_level_xp
        return max(0, XP_PER_LEVEL - xp_in_level)

    @property
    def xp_progress(self):
        current_level_xp = (self.level - 1) * XP_PER_LEVEL
        xp_in_level = self.xp - current_level_xp
        return min(100, int((xp_in_level / XP_PER_LEVEL) * 100))

    @property
    def level_title(self):
        titles = {
            range(1, 6): '🏠 宅家新手',
            range(6, 11): '🚶 出门散步',
            range(11, 16): '🏃 初级跑者',
            range(16, 21): '💪 健身学徒',
            range(21, 26): '🏋️ 力量觉醒',
            range(26, 31): '⚔️ 战斗勇士',
            range(31, 36): '🛡️ 铁壁骑士',
            range(36, 41): '🐉 龙之传人',
            range(41, 46): '👑 健身王者',
            range(46, 51): '🌟 传说勇者',
        }
        for level_range, title in titles.items():
            if self.level in level_range:
                return title
        return '🏆 超越极限'

    def add_xp(self, amount, activity_type='exercise'):
        self.xp += amount
        new_level = (self.xp // XP_PER_LEVEL) + 1
        leveled_up = new_level > self.level
        self.level = new_level

        if activity_type == 'exercise':
            self.strength = min(100, self.strength + 1)
        elif activity_type == 'meal':
            self.willpower = min(100, self.willpower + 1)
        elif activity_type == 'sleep':
            self.endurance = min(100, self.endurance + 1)

        self.save()
        return leveled_up


class Achievement(models.Model):
    ACHIEVEMENT_TYPES = (
        ('checkin', '打卡成就'),
        ('meal', '饮食成就'),
        ('sleep', '睡眠成就'),
        ('social', '趣味成就'),
        ('special', '特殊成就'),
    )

    name = models.CharField(max_length=100, verbose_name='成就名称')
    description = models.TextField(verbose_name='成就描述')
    icon = models.CharField(max_length=50, default='🏆', verbose_name='图标')
    category = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES, verbose_name='分类')
    xp_reward = models.IntegerField(default=50, verbose_name='经验奖励')

    condition_type = models.CharField(max_length=50, verbose_name='条件类型')
    condition_value = models.IntegerField(default=1, verbose_name='条件数值')

    is_hidden = models.BooleanField(default=False, verbose_name='隐藏成就')
    order = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        verbose_name = '成就'
        verbose_name_plural = '成就列表'
        ordering = ['category', 'order']

    def __str__(self):
        return f'{self.icon} {self.name}'


class UserAchievement(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='achievements'
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        verbose_name='成就'
    )
    unlocked_at = models.DateTimeField(auto_now_add=True, verbose_name='解锁时间')

    class Meta:
        verbose_name = '用户成就'
        verbose_name_plural = '用户成就列表'
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f'{self.user.username} - {self.achievement.name}'


class DailyMission(models.Model):
    MISSION_TYPES = (
        ('checkin', '运动打卡'),
        ('duration', '运动时长'),
        ('meal', '三餐记录'),
        ('sleep', '早睡挑战'),
    )

    title = models.CharField(max_length=200, verbose_name='任务标题')
    description = models.TextField(verbose_name='任务描述')
    mission_type = models.CharField(max_length=20, choices=MISSION_TYPES, verbose_name='任务类型')
    target_value = models.IntegerField(default=1, verbose_name='目标值')
    xp_reward = models.IntegerField(default=30, verbose_name='经验奖励')
    is_active = models.BooleanField(default=True, verbose_name='激活状态')
    order = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        verbose_name = '每日任务'
        verbose_name_plural = '每日任务列表'
        ordering = ['order']

    def __str__(self):
        return self.title


class UserDailyMission(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='daily_missions'
    )
    mission = models.ForeignKey(
        DailyMission,
        on_delete=models.CASCADE,
        verbose_name='任务'
    )
    date = models.DateField(default=timezone.now, verbose_name='日期')
    progress = models.IntegerField(default=0, verbose_name='当前进度')
    completed = models.BooleanField(default=False, verbose_name='已完成')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')

    class Meta:
        verbose_name = '用户每日任务'
        verbose_name_plural = '用户每日任务列表'
        unique_together = ('user', 'mission', 'date')

    def __str__(self):
        return f'{self.user.username} - {self.mission.title} - {self.date}'
