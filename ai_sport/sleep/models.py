"""
睡眠记录模块数据模型

本模块定义了睡眠记录功能的数据模型，用于追踪用户的睡眠质量和时长。
每个睡眠记录关联到特定用户，包含入睡时间、起床时间、睡眠质量等信息。

主要功能：
- 记录用户每日睡眠情况
- 追踪入睡和起床时间
- 记录睡眠质量评级
- 自动计算睡眠时长
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SleepRecord(models.Model):
    """
    睡眠记录模型

    用于存储用户的睡眠记录，包括入睡时间、起床时间、睡眠质量和时长等信息。
    每条睡眠记录关联到一个用户，用户删除时其所有睡眠记录也会被删除。

    Attributes:
        user: 关联的用户，外键指向Django内置User模型
        date: 记录日期（通常是起床日期）
        sleep_time: 入睡时间
        wake_time: 起床时间
        quality: 睡眠质量评级
        duration: 计算得出的睡眠时长（小时）
        notes: 用户添加的备注信息
        created_at: 记录创建时间，由Django自动设置
    """

    # 睡眠质量评级选项
    SLEEP_QUALITY = (
        ('excellent', '优秀'),
        ('good', '良好'),
        ('fair', '一般'),
        ('poor', '较差'),
    )
    """
    睡眠质量评级选项

    定义四种睡眠质量等级：
    - excellent: 优秀，睡眠质量很高，起床后精神充沛
    - good: 良好，睡眠质量较好
    - fair: 一般，睡眠质量一般，可能有些疲惫
    - poor: 较差，睡眠质量不好，起床后仍感疲惫
    """

    # 关联用户，外键级联删除
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='sleep_records'
    )

    # 记录日期，默认为当前日期
    date = models.DateField(
        default=timezone.now,
        verbose_name='记录日期'
    )

    # 入睡时间
    sleep_time = models.TimeField(
        verbose_name='入睡时间',
        help_text='记录昨晚入睡的时间'
    )

    # 起床时间
    wake_time = models.TimeField(
        verbose_name='起床时间',
        help_text='记录今天起床的时间'
    )

    # 睡眠质量评级，默认为"一般"
    quality = models.CharField(
        max_length=20,
        choices=SLEEP_QUALITY,
        default='fair',
        verbose_name='睡眠质量'
    )

    # 睡眠时长，单位为小时，可由系统自动计算
    duration = models.FloatField(
        null=True,
        blank=True,
        verbose_name='睡眠时长（小时）',
        help_text='系统自动计算，或手动输入睡眠时长'
    )

    # 备注信息
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='备注',
        help_text='添加任何其他想记录的信息，如做梦情况、中途醒来等'
    )

    # 记录创建时间
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    class Meta:
        """
        模型的元数据配置

        verbose_name: 模型的单数中文名称
        verbose_name_plural: 模型的复数中文名称
        ordering: 默认排序方式，按日期降序（最新在前）
        """
        verbose_name = '睡眠记录'
        verbose_name_plural = '睡眠记录列表'
        ordering = ['-date']

    def __str__(self):
        """
        返回睡眠记录的中文字符串表示

        格式为"用户名 - 日期 - 质量"，如"张三 - 2024-01-15 - 良好"
        用于在Django Admin和管理界面中清晰显示睡眠信息
        """
        return f'{self.user.username} - {self.date} - {self.get_quality_display()}'

    def get_quality_display(self):
        """
        获取睡眠质量的中文显示名称

        将数据库中存储的英文质量代码（如'excellent'）转换为中文显示（如'优秀'）

        Returns:
            str: 睡眠质量对应的中文名称
        """
        return dict(self.SLEEP_QUALITY).get(self.quality, self.quality)

    def calculate_duration(self):
        """
        计算睡眠时长

        根据入睡时间和起床时间自动计算睡眠时长。
        支持跨午夜计算（例如：23:00入睡，次日07:00起床）。

        Returns:
            float: 睡眠时长，单位为小时
        """
        from datetime import datetime, timedelta

        sleep_dt = datetime.combine(self.date, self.sleep_time)
        wake_dt = datetime.combine(self.date, self.wake_time)

        if wake_dt < sleep_dt:
            wake_dt += timedelta(days=1)

        duration_hours = (wake_dt - sleep_dt).total_seconds() / 3600
        return round(duration_hours, 1)