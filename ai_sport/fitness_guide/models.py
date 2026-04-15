"""
健身指南模块数据模型

本模块定义了健身指南相关的所有数据模型，包括器材信息、饮食建议和肌肉认识等。
每个器材可以归属于不同的类别（有氧器材、力量训练器材、功能性训练器材）。
饮食建议分为不同的类别。
肌肉认识分为不同的肌群和肌肉部位。
"""

from django.db import models


class Equipment(models.Model):
    """
    器材模型

    用于存储健身房器材的详细信息，包括器材名称、类别、图片、视频链接和描述。
    器材分为三大类别：有氧器材、力量训练器材、功能性训练器材。
    """

    EQUIPMENT_CATEGORIES = (
        ('cardio', '有氧器材'),
        ('strength', '力量训练器材'),
        ('functional', '功能性训练器材'),
    )

    name = models.CharField(max_length=100, verbose_name='器材名称')
    category = models.CharField(max_length=20, choices=EQUIPMENT_CATEGORIES, verbose_name='器材类别')
    image = models.ImageField(upload_to='equipment_images/', null=True, blank=True, verbose_name='器材图片')
    video_url = models.URLField(max_length=500, null=True, blank=True, verbose_name='视频链接')
    description = models.TextField(null=True, blank=True, verbose_name='器材描述')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '器材'
        verbose_name_plural = '器材列表'
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.get_category_display()} - {self.name}'

    def get_category_display(self):
        return dict(self.EQUIPMENT_CATEGORIES).get(self.category, self.category)


class DietItem(models.Model):
    """
    饮食建议模型

    用于存储健身饮食相关的建议内容，包括标题、详细描述、图片和视频链接。
    饮食建议分为不同的类别：健身前饮食、健身后饮食、日常营养等。
    """

    DIET_CATEGORIES = (
        ('pre_workout', '健身前饮食'),
        ('post_workout', '健身后饮食'),
        ('daily_nutrition', '日常营养'),
        ('supplement', '营养补剂'),
        ('tips', '饮食小贴士'),
    )

    title = models.CharField(max_length=200, verbose_name='标题')
    category = models.CharField(max_length=20, choices=DIET_CATEGORIES, verbose_name='类别')
    image = models.ImageField(upload_to='diet_images/', null=True, blank=True, verbose_name='配图')
    video_url = models.URLField(max_length=500, null=True, blank=True, verbose_name='视频链接')
    content = models.TextField(verbose_name='详细内容')
    is_featured = models.BooleanField(default=False, verbose_name='推荐显示')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '饮食建议'
        verbose_name_plural = '饮食建议列表'
        ordering = ['category', '-created_at']

    def __str__(self):
        return f'{self.get_category_display()} - {self.title}'

    def get_category_display(self):
        return dict(self.DIET_CATEGORIES).get(self.category, self.category)


class MuscleGroup(models.Model):
    """
    肌肉群模型

    用于存储人体主要肌肉群的分类信息。
    每个肌肉群包含多个具体的肌肉部位。

    Attributes:
        name: 肌肉群名称（如：胸部、背部、腿部等）
        latin_name: 拉丁学名
        icon: 图标emoji
        description: 简要描述
        created_at: 创建时间
    """

    MUSCLE_GROUP_CATEGORIES = (
        ('upper', '上肢肌群'),
        ('core', '核心肌群'),
        ('lower', '下肢肌群'),
        ('cardio', '心肺功能'),
    )

    name = models.CharField(
        max_length=100,
        verbose_name='肌肉群名称',
        help_text='如：胸部、背部、肩部、手臂、腿部等'
    )

    latin_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='拉丁学名',
        help_text='肌肉群的拉丁学名'
    )

    category = models.CharField(
        max_length=20,
        choices=MUSCLE_GROUP_CATEGORIES,
        verbose_name='所属大类',
        help_text='选择肌肉群所属的类别'
    )

    icon = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='图标',
        help_text='输入emoji图标，如：💪、🏋️等'
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='简要描述',
        help_text='简要描述该肌肉群的位置和功能'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '肌肉群'
        verbose_name_plural = '肌肉群列表'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class MuscleItem(models.Model):
    """
    肌肉部位模型

    用于存储具体肌肉部位的详细信息，包括名称、描述、训练动作、图片和视频链接。
    每个肌肉部位归属于一个肌肉群。

    Attributes:
        muscle_group: 所属肌肉群，外键关联
        name: 肌肉部位名称
        latin_name: 拉丁学名
        image: 肌肉部位图片
        video_url: 教学视频链接
        description: 详细描述
        training_tips: 训练要点
        is_featured: 是否推荐显示
        created_at: 创建时间
        updated_at: 更新时间
    """

    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.CASCADE,
        verbose_name='所属肌肉群',
        related_name='muscle_items'
    )

    name = models.CharField(
        max_length=100,
        verbose_name='肌肉部位名称',
        help_text='如：胸大肌、背阔肌、股四头肌等'
    )

    latin_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='拉丁学名',
        help_text='肌肉部位的拉丁学名'
    )

    image = models.ImageField(
        upload_to='muscle_images/',
        null=True,
        blank=True,
        verbose_name='肌肉图片',
        help_text='上传肌肉部位的图片'
    )

    video_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='视频链接',
        help_text='输入相关的训练视频链接'
    )

    description = models.TextField(
        verbose_name='详细描述',
        help_text='详细描述该肌肉的位置、功能和训练方法'
    )

    training_tips = models.TextField(
        null=True,
        blank=True,
        verbose_name='训练要点',
        help_text='输入该肌肉的训练要点和注意事项'
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name='推荐显示',
        help_text='勾选后在首页推荐显示'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '肌肉部位'
        verbose_name_plural = '肌肉部位列表'
        ordering = ['muscle_group', 'name']

    def __str__(self):
        return f'{self.muscle_group.name} - {self.name}'