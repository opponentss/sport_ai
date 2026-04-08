# 健身打卡软件 - 完整数据查询指南

## 一、查询方式概览

### 1.1 四种查询途径
1. **Django管理后台** (`/admin/`) - 管理员专用，完整数据访问权限
2. **Web用户界面** - 普通用户通过浏览器访问自己的数据
3. **Django Shell** - 开发调试，直接数据库操作
4. **API接口** - 未来可扩展REST API供第三方调用

### 1.2 核心查询工具
- **Django ORM**：主要查询方式，安全高效，防止SQL注入
- **原始SQL**：复杂统计分析时使用
- **Django QuerySet API**：丰富的链式查询方法

## 二、Django ORM 基础查询

### 2.1 基本查询语法

```python
# 导入模型
from checkin.models import Checkin
from meals.models import Meal
from sleep.models import SleepRecord
from django.contrib.auth.models import User

# 1. 获取所有记录
all_checkins = Checkin.objects.all()

# 2. 获取单个记录（通过主键）
checkin = Checkin.objects.get(pk=1)

# 3. 过滤查询（最常用）
user_checkins = Checkin.objects.filter(user=request.user)

# 4. 排除查询
other_checkins = Checkin.objects.exclude(user=request.user)

# 5. 排序查询
sorted_checkins = Checkin.objects.order_by('-created_at')  # 降序
sorted_checkins = Checkin.objects.order_by('date')         # 升序
```

### 2.2 常用查询方法速查表

| 方法 | 描述 | 示例 |
|------|------|------|
| `all()` | 获取所有记录 | `Checkin.objects.all()` |
| `get()` | 获取单个记录 | `Checkin.objects.get(pk=1)` |
| `filter()` | 过滤记录 | `Checkin.objects.filter(user=user)` |
| `exclude()` | 排除记录 | `Checkin.objects.exclude(user=user)` |
| `order_by()` | 排序 | `Checkin.objects.order_by('-date')` |
| `count()` | 计数 | `Checkin.objects.count()` |
| `first()` | 第一条 | `Checkin.objects.first()` |
| `last()` | 最后一条 | `Checkin.objects.last()` |
| `exists()` | 是否存在 | `Checkin.objects.filter(user=user).exists()` |
| `distinct()` | 去重 | `Checkin.objects.values('activity').distinct()` |

## 三、用户数据查询

### 3.1 用户基本信息查询

```python
from django.contrib.auth.models import User

# 1. 获取当前登录用户（在视图中）
current_user = request.user

# 2. 通过用户名查询用户
user = User.objects.get(username='john_doe')

# 3. 通过邮箱查询用户
user = User.objects.get(email='john@example.com')

# 4. 查询活跃用户
active_users = User.objects.filter(is_active=True)

# 5. 查询管理员用户
admin_users = User.objects.filter(is_staff=True)

# 6. 查询超级用户
superusers = User.objects.filter(is_superuser=True)

# 7. 用户统计
total_users = User.objects.count()
active_count = User.objects.filter(is_active=True).count()
```

### 3.2 用户关联数据查询

```python
# 1. 获取用户的所有打卡记录（反向查询）
user_checkins = request.user.checkin_set.all()

# 2. 获取用户的所有饮食记录
user_meals = request.user.meal_set.all()

# 3. 获取用户的所有睡眠记录
user_sleep_records = request.user.sleeprecord_set.all()

# 4. 使用反向关系带条件查询
user = User.objects.get(username='john_doe')
recent_checkins = user.checkin_set.filter(date__gte='2024-03-01')
```

## 四、打卡记录查询

### 4.1 基础查询

```python
from checkin.models import Checkin
from django.utils import timezone
from datetime import datetime, timedelta

# 1. 查询用户的所有打卡记录
user_checkins = Checkin.objects.filter(user=request.user)

# 2. 按活动类型查询
running_checkins = Checkin.objects.filter(
    user=request.user, 
    activity='跑步'
)

# 3. 按时长范围查询
long_checkins = Checkin.objects.filter(
    user=request.user,
    duration__gte=60  # 时长大于等于60分钟
)

short_checkins = Checkin.objects.filter(
    user=request.user,
    duration__lte=30  # 时长小于等于30分钟
)
```

### 4.2 时间范围查询

```python
from datetime import date, timedelta

# 1. 查询今日打卡记录
today = timezone.now().date()
today_checkins = Checkin.objects.filter(
    user=request.user,
    date=today
)

# 2. 查询最近7天打卡记录
week_ago = timezone.now().date() - timedelta(days=7)
recent_checkins = Checkin.objects.filter(
    user=request.user,
    date__gte=week_ago
)

# 3. 查询本月打卡记录
current_month = timezone.now().month
current_year = timezone.now().year
monthly_checkins = Checkin.objects.filter(
    user=request.user,
    date__year=current_year,
    date__month=current_month
)

# 4. 查询特定日期范围的记录
start_date = date(2024, 3, 1)
end_date = date(2024, 3, 31)
march_checkins = Checkin.objects.filter(
    user=request.user,
    date__range=[start_date, end_date]
)
```

### 4.3 地理位置查询

```python
# 1. 查询有位置信息的打卡记录
located_checkins = Checkin.objects.filter(
    user=request.user,
    latitude__isnull=False,
    longitude__isnull=False
)

# 2. 查询特定位置的打卡记录
beijing_checkins = Checkin.objects.filter(
    user=request.user,
    location__icontains='北京'
)

# 3. 查询位置半径内的记录（近似查询）
target_lat = 39.9042
target_lng = 116.4074
radius = 0.1  # 约11公里

nearby_checkins = Checkin.objects.filter(
    user=request.user,
    latitude__range=(target_lat - radius, target_lat + radius),
    longitude__range=(target_lng - radius, target_lng + radius)
)
```

## 五、饮食记录查询

### 5.1 基础查询

```python
from meals.models import Meal

# 1. 查询用户的所有饮食记录
user_meals = Meal.objects.filter(user=request.user)

# 2. 按餐食类型查询
breakfasts = Meal.objects.filter(
    user=request.user,
    meal_type='breakfast'
)

lunches = Meal.objects.filter(
    user=request.user,
    meal_type='lunch'
)

dinners = Meal.objects.filter(
    user=request.user,
    meal_type='dinner'
)

# 3. 查询有图片的记录
meals_with_images = Meal.objects.filter(
    user=request.user,
    image__isnull=False
)

# 4. 查询有卡路里信息的记录
meals_with_calories = Meal.objects.filter(
    user=request.user,
    calories__isnull=False
)
```

### 5.2 营养信息查询

```python
# 1. 查询高卡路里饮食
high_calorie_meals = Meal.objects.filter(
    user=request.user,
    calories__gte=500
)

# 2. 查询低卡路里饮食
low_calorie_meals = Meal.objects.filter(
    user=request.user,
    calories__lte=300
)

# 3. 查询特定卡路里范围的饮食
medium_calorie_meals = Meal.objects.filter(
    user=request.user,
    calories__range=(300, 500)
)

# 4. 统计总卡路里摄入
from django.db.models import Sum
total_calories = Meal.objects.filter(
    user=request.user,
    date=timezone.now().date()
).aggregate(total=Sum('calories'))['total'] or 0
```

## 六、睡眠记录查询

### 6.1 基础查询

```python
from sleep.models import SleepRecord

# 1. 查询用户的所有睡眠记录
user_sleep_records = SleepRecord.objects.filter(user=request.user)

# 2. 按睡眠质量查询
good_sleep = SleepRecord.objects.filter(
    user=request.user,
    quality='good'
)

excellent_sleep = SleepRecord.objects.filter(
    user=request.user,
    quality='excellent'
)

# 3. 查询有备注的记录
sleep_with_notes = SleepRecord.objects.filter(
    user=request.user,
    notes__isnull=False
)
```

### 6.2 睡眠时长查询

```python
# 1. 查询充足睡眠（>=7小时）
good_duration_sleep = SleepRecord.objects.filter(
    user=request.user,
    duration__gte=7.0
)

# 2. 查询不足睡眠（<6小时）
poor_duration_sleep = SleepRecord.objects.filter(
    user=request.user,
    duration__lt=6.0
)

# 3. 查询特定时长范围的睡眠
medium_duration_sleep = SleepRecord.objects.filter(
    user=request.user,
    duration__range=(6.0, 8.0)
)

# 4. 计算平均睡眠时长
from django.db.models import Avg
avg_sleep_duration = SleepRecord.objects.filter(
    user=request.user
).aggregate(avg=Avg('duration'))['avg'] or 0
```

## 七、高级查询技巧

### 7.1 字段查询（Field Lookups）完整列表

| 查找类型 | 描述 | 示例 |
|----------|------|------|
| `exact` | 精确匹配 | `activity__exact='跑步'` |
| `iexact` | 不区分大小写精确匹配 | `activity__iexact='running'` |
| `contains` | 包含 | `location__contains='北京'` |
| `icontains` | 不区分大小写包含 | `location__icontains='beijing'` |
| `in` | 在列表中 | `activity__in=['跑步', '游泳', '健身']` |
| `gt` | 大于 | `duration__gt=60` |
| `gte` | 大于等于 | `duration__gte=30` |
| `lt` | 小于 | `calories__lt=500` |
| `lte` | 小于等于 | `calories__lte=300` |
| `startswith` | 以...开头 | `activity__startswith='跑'` |
| `istartswith` | 不区分大小写以...开头 | `activity__istartswith='run'` |
| `endswith` | 以...结尾 | `location__endswith='区'` |
| `iendswith` | 不区分大小写以...结尾 | `location__iendswith='district'` |
| `range` | 范围 | `date__range=[start_date, end_date]` |
| `date` | 日期字段查询 | `date__year=2024`, `date__month=3` |
| `isnull` | 是否为NULL | `image__isnull=True` |
| `regex` | 正则匹配 | `activity__regex=r'^跑.*'` |
| `iregex` | 不区分大小写正则匹配 | `activity__iregex=r'^run.*'` |

### 7.2 Q对象复杂查询

```python
from django.db.models import Q

# 1. OR查询：跑步或游泳
running_or_swimming = Checkin.objects.filter(
    Q(activity='跑步') | Q(activity='游泳')
)

# 2. AND查询：跑步且时长大于30分钟
running_long = Checkin.objects.filter(
    Q(activity='跑步') & Q(duration__gt=30)
)

# 3. 复杂组合查询
complex_query = Checkin.objects.filter(
    Q(activity='跑步', duration__gte=30) |
    Q(activity='游泳', duration__gte=45) |
    Q(activity='健身', duration__gte=60)
)

# 4. NOT查询
not_running = Checkin.objects.filter(
    ~Q(activity='跑步')
)
```

### 7.3 聚合查询与统计

```python
from django.db.models import Count, Sum, Avg, Max, Min

# 1. 基本聚合
checkin_stats = Checkin.objects.filter(
    user=request.user
).aggregate(
    total=Count('id'),
    avg_duration=Avg('duration'),
    max_duration=Max('duration'),
    min_duration=Min('duration')
)

# 2. 分组统计
activity_stats = Checkin.objects.filter(
    user=request.user
).values('activity').annotate(
    count=Count('id'),
    avg_duration=Avg('duration')
).order_by('-count')

# 3. 每日统计
daily_stats = Checkin.objects.filter(
    user=request.user
).values('date').annotate(
    count=Count('id'),
    total_duration=Sum('duration')
).order_by('-date')
```

## 八、查询优化技巧

### 8.1 select_related（预加载外键关联）

```python
# 1. 预加载用户信息，减少查询次数
checkins_with_user = Checkin.objects.select_related('user').all()
# 访问用户信息时不会产生额外查询
for checkin in checkins_with_user:
    print(checkin.user.username)  # 无额外数据库查询

# 2. 预加载多个关联
meals_with_user = Meal.objects.select_related('user').filter(
    date=timezone.now().date()
)
```

### 8.2 prefetch_related（预加载多对多、反向关联）

```python
# 1. 预加载用户的打卡记录
users_with_checkins = User.objects.prefetch_related('checkin_set').all()
for user in users_with_checkins:
    # 访问打卡记录时不会产生额外查询
    checkins = user.checkin_set.all()

# 2. 预加载多个关联
from django.db.models import Prefetch
users_with_all_data = User.objects.prefetch_related(
    Prefetch('checkin_set', queryset=Checkin.objects.order_by('-date')),
    Prefetch('meal_set', queryset=Meal.objects.order_by('-date')),
    Prefetch('sleeprecord_set', queryset=SleepRecord.objects.order_by('-date'))
)
```

### 8.3 查询性能优化

```python
# 1. 只选择需要的字段（减少数据传输）
checkins_light = Checkin.objects.only('id', 'activity', 'date', 'duration')

# 2. 延迟加载大字段
meals_without_images = Meal.objects.defer('image')

# 3. 使用values()获取字典列表（更轻量）
checkin_dicts = Checkin.objects.values('id', 'activity', 'date', 'duration')

# 4. 使用values_list()获取元组列表（最轻量）
checkin_tuples = Checkin.objects.values_list('id', 'activity', 'date')

# 5. 限制返回数量
recent_checkins = Checkin.objects.filter(
    user=request.user
).order_by('-date')[:50]  # 只返回最近50条
```

## 九、Django Shell 实践查询

### 9.1 启动和基本操作

```bash
# 进入项目目录
cd ai_sport

# 启动Django Shell
python manage.py shell
```

### 9.2 Shell查询示例

```python
# 1. 导入必要的模块
from django.contrib.auth.models import User
from checkin.models import Checkin
from meals.models import Meal
from sleep.models import SleepRecord
from django.utils import timezone
from datetime import timedelta

# 2. 查询测试用户
test_user = User.objects.get(username='testuser')

# 3. 查询用户的所有数据
print("=== 用户数据统计 ===")
print(f"用户名: {test_user.username}")
print(f"邮箱: {test_user.email}")

checkin_count = Checkin.objects.filter(user=test_user).count()
meal_count = Meal.objects.filter(user=test_user).count()
sleep_count = SleepRecord.objects.filter(user=test_user).count()

print(f"打卡记录数: {checkin_count}")
print(f"饮食记录数: {meal_count}")
print(f"睡眠记录数: {sleep_count}")

# 4. 查询最近7天的数据
week_ago = timezone.now().date() - timedelta(days=7)

recent_checkins = Checkin.objects.filter(
    user=test_user,
    date__gte=week_ago
).order_by('-date')

print(f"\n=== 最近7天打卡记录 ===")
for checkin in recent_checkins:
    print(f"{checkin.date}: {checkin.activity} - {checkin.duration}分钟")
```

### 9.3 数据导出功能

```python
# 导出用户数据到CSV
import csv
from datetime import datetime

def export_user_data(user_id, filename):
    """导出用户所有数据到CSV文件"""
    user = User.objects.get(id=user_id)
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # 写入打卡记录
        writer.writerow(['=== 打卡记录 ==='])
        writer.writerow(['日期', '活动', '时长(分钟)', '位置', '备注'])
        
        checkins = Checkin.objects.filter(user=user).order_by('-date')
        for checkin in checkins:
            writer.writerow([
                check