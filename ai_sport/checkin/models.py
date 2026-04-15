"""
运动打卡模块数据模型

本模块定义了运动打卡功能的数据模型，用于记录用户的运动活动。
每个打卡记录关联到特定用户，包含活动类型、时长、位置等信息。

主要功能：
- 记录用户运动打卡信息
- 支持GPS定位记录运动地点
- 记录运动时长和详细备注
"""

from django.db import models
from django.contrib.auth.models import User


class Checkin(models.Model):
    """
    运动打卡模型

    用于存储用户的运动打卡记录，包括活动类型、时长、日期时间、位置信息等。
    每条打卡记录关联到一个用户，用户删除时其所有打卡记录也会被删除。

    Attributes:
        user: 关联的用户，外键指向Django内置User模型
        activity: 运动活动名称，如"跑步"、"游泳"、"健身"等
        duration: 活动时长，单位为分钟
        date: 打卡日期，由系统自动设置（首次创建时）
        time: 打卡时间，由系统自动设置（首次创建时）
        latitude: GPS纬度坐标，用于记录运动地点
        longitude: GPS经度坐标，用于记录运动地点
        location: 位置描述文字，如"XX健身房"、"XX公园"等
        notes: 用户添加的备注信息
        created_at: 记录创建时间，由Django自动设置
    """

    # 关联用户，外键级联删除（用户删除时，打卡记录一并删除）
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='checkins'
    )

    # 运动活动名称
    activity = models.CharField(
        max_length=100,
        verbose_name='活动名称',
        help_text='输入运动项目名称，如"跑步"、"游泳"、"健身"等'
    )

    # 活动时长，单位分钟
    duration = models.IntegerField(
        verbose_name='活动时长（分钟）',
        help_text='输入活动持续时间，单位为分钟'
    )

    # 打卡日期，首次创建时自动设置为当前日期
    date = models.DateField(
        auto_now_add=True,
        verbose_name='打卡日期'
    )

    # 打卡时间，首次创建时自动设置为当前时间
    time = models.TimeField(
        auto_now_add=True,
        verbose_name='打卡时间'
    )

    # GPS定位功能 - 纬度
    latitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='纬度',
        help_text='GPS纬度坐标，可通过地图获取'
    )

    # GPS定位功能 - 经度
    longitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='经度',
        help_text='GPS经度坐标，可通过地图获取'
    )

    # 位置描述文字
    location = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='位置描述',
        help_text='输入位置名称，如"XX健身房"、"XX公园"'
    )

    # 备注信息
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='备注',
        help_text='添加任何其他想记录的信息'
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
        verbose_name = '运动打卡'
        verbose_name_plural = '运动打卡记录'
        ordering = ['-date', '-time']

    def __str__(self):
        """
        返回打卡记录的中文字符串表示

        格式为"用户名 - 活动名称 - 日期"，如"张三 - 跑步 - 2024-01-15"
        用于在Django Admin和管理界面中清晰显示打卡信息
        """
        return f'{self.user.username} - {self.activity} - {self.date}'