"""
餐饮管理模块数据模型

本模块定义了餐饮记录功能的数据模型，用于记录用户的饮食摄入情况。
每个餐饮记录关联到特定用户，包含餐食类型、营养信息、图片等。

主要功能：
- 记录用户三餐摄入情况
- 支持拍照上传餐食图片
- 记录卡路里摄入
- 记录用餐时间和描述
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Meal(models.Model):
    """
    餐饮记录模型

    用于存储用户的餐饮记录，包括餐食类型、日期时间、图片、描述和卡路里信息。
    每条餐饮记录关联到一个用户，用户删除时其所有餐饮记录也会被删除。

    Attributes:
        user: 关联的用户，外键指向Django内置User模型
        meal_type: 餐食类型（早餐/午餐/晚餐）
        date: 用餐日期
        time: 用餐时间
        image: 餐食照片，支持图片上传
        description: 餐食描述和详情
        calories: 摄入卡路里数量
        created_at: 记录创建时间，由Django自动设置
    """

    # 餐食类型选项
    MEAL_TYPES = (
        ('breakfast', '早餐'),
        ('lunch', '午餐'),
        ('dinner', '晚餐'),
    )
    """
    餐食类型选项

    定义一日三餐的类型：
    - breakfast: 早餐，通常在早上6-10点
    - lunch: 午餐，通常在中午11-14点
    - dinner: 晚餐，通常在晚上17-20点
    """

    # 关联用户，外键级联删除
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='meals'
    )

    # 餐食类型，从预定义选项中选择
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPES,
        verbose_name='餐食类型'
    )

    # 用餐日期，默认为当前日期
    date = models.DateField(
        default=timezone.now,
        verbose_name='用餐日期'
    )

    # 用餐时间，默认为当前时间
    time = models.TimeField(
        default=timezone.now,
        verbose_name='用餐时间'
    )

    # 餐食图片，支持JPG/PNG格式，上传到meal_images/目录
    image = models.ImageField(
        upload_to='meal_images/',
        null=True,
        blank=True,
        verbose_name='餐食图片',
        help_text='上传餐食照片，支持JPG、PNG格式'
    )

    # 餐食描述
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='餐食描述',
        help_text='描述这餐吃了什么食物'
    )

    # 卡路里摄入数量
    calories = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='卡路里',
        help_text='输入这餐摄入的卡路里数量'
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
        verbose_name = '餐饮记录'
        verbose_name_plural = '餐饮记录列表'
        ordering = ['-date', '-time']

    def __str__(self):
        """
        返回餐饮记录的中文字符串表示

        格式为"用户名 - 餐食类型 - 日期"，如"张三 - 午餐 - 2024-01-15"
        用于在Django Admin和管理界面中清晰显示餐饮信息
        """
        return f'{self.user.username} - {self.get_meal_type_display()} - {self.date}'

    def get_meal_type_display(self):
        """
        获取餐食类型的中文显示名称

        将数据库中存储的英文类型代码（如'breakfast'）转换为中文显示（如'早餐'）

        Returns:
            str: 餐食类型对应的中文名称
        """
        return dict(self.MEAL_TYPES).get(self.meal_type, self.meal_type)