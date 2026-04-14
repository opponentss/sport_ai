from django.db import models

class Equipment(models.Model):
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