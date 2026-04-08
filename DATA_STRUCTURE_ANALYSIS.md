# 健身打卡软件 - 数据结构和存储位置分析

## 项目概述
健身打卡软件是一个基于Django的Web应用，包含三个核心功能模块：打卡记录、饮食记录、睡眠记录。项目使用PostgreSQL作为主数据库，Redis作为缓存，支持Docker容器化部署。

## 一、数据库架构

### 1.1 数据库类型
- **主数据库**: PostgreSQL 16 (生产环境) / SQLite3 (开发环境)
- **缓存数据库**: Redis 7
- **文件存储**: 本地文件系统 (媒体文件)

### 1.2 数据库连接配置
```python
# settings.py 中的数据库配置
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # 使用 PostgreSQL（生产环境）
    DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}
else:
    # 默认使用 SQLite（开发环境）
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
```

## 二、数据模型结构

### 2.1 用户认证系统 (Django内置)
**存储位置**: `auth_*` 表系列

| 表名 | 字段 | 描述 |
|------|------|------|
| `auth_user` | `id`, `username`, `password`, `email`, `first_name`, `last_name`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined` | 用户基本信息表 |
| `auth_group` | `id`, `name` | 用户组表 |
| `auth_permission` | `id`, `name`, `content_type_id`, `codename` | 权限表 |
| `auth_user_groups` | `id`, `user_id`, `group_id` | 用户-组关联表 |
| `auth_user_user_permissions` | `id`, `user_id`, `permission_id` | 用户-权限关联表 |

### 2.2 打卡记录模块 (checkin应用)
**存储位置**: `checkin_checkin` 表

| 字段 | 类型 | 描述 | 约束 |
|------|------|------|------|
| `id` | BigAutoField | 主键 | PRIMARY KEY |
| `user_id` | ForeignKey | 关联用户 | NOT NULL, CASCADE |
| `activity` | CharField(100) | 活动名称 | NOT NULL |
| `duration` | IntegerField | 活动时长(分钟) | NOT NULL |
| `date` | DateField | 打卡日期 | auto_now_add=True |
| `time` | TimeField | 打卡时间 | auto_now_add=True |
| `latitude` | FloatField | 纬度坐标 | NULLABLE |
| `longitude` | FloatField | 经度坐标 | NULLABLE |
| `location` | CharField(200) | 位置描述 | NULLABLE |
| `notes` | TextField | 备注 | NULLABLE |
| `created_at` | DateTimeField | 创建时间 | auto_now_add=True |

**索引**:
- 自动创建: `user_id` 外键索引
- 建议索引: `(user_id, date)` 复合索引用于查询用户每日打卡记录

### 2.3 饮食记录模块 (meals应用)
**存储位置**: `meals_meal` 表

| 字段 | 类型 | 描述 | 约束 |
|------|------|------|------|
| `id` | BigAutoField | 主键 | PRIMARY KEY |
| `user_id` | ForeignKey | 关联用户 | NOT NULL, CASCADE |
| `meal_type` | CharField(20) | 餐食类型 | choices: breakfast/lunch/dinner |
| `date` | DateField | 记录日期 | default=timezone.now |
| `time` | TimeField | 记录时间 | default=timezone.now |
| `image` | ImageField | 食物图片 | upload_to='meal_images/' |
| `description` | TextField | 食物描述 | NULLABLE |
| `calories` | IntegerField | 卡路里 | NULLABLE |
| `created_at` | DateTimeField | 创建时间 | auto_now_add=True |

**枚举值**:
- `meal_type`: `breakfast`(早餐), `lunch`(午餐), `dinner`(晚餐)

**文件存储**:
- 图片路径: `media/meal_images/YYYY/MM/DD/filename.ext`
- 使用Django的`ImageField`自动处理文件上传

### 2.4 睡眠记录模块 (sleep应用)
**存储位置**: `sleep_sleeprecord` 表

| 字段 | 类型 | 描述 | 约束 |
|------|------|------|------|
| `id` | BigAutoField | 主键 | PRIMARY KEY |
| `user_id` | ForeignKey | 关联用户 | NOT NULL, CASCADE |
| `date` | DateField | 记录日期 | default=timezone.now |
| `sleep_time` | TimeField | 入睡时间 | NOT NULL |
| `wake_time` | TimeField | 起床时间 | NOT NULL |
| `quality` | CharField(20) | 睡眠质量 | choices: excellent/good/fair/poor |
| `duration` | FloatField | 睡眠时长(小时) | NULLABLE |
| `notes` | TextField | 备注 | NULLABLE |
| `created_at` | DateTimeField | 创建时间 | auto_now_add=True |

**枚举值**:
- `quality`: `excellent`(优秀), `good`(良好), `fair`(一般), `poor`(较差)

**计算字段**:
- `duration`: 可通过`wake_time`和`sleep_time`计算得出

## 三、数据关系图

```
用户 (auth_user)
    │
    ├─── 1:N ─── 打卡记录 (checkin_checkin)
    │       ├── activity: 活动名称
    │       ├── duration: 时长
    │       └── location: 位置信息
    │
    ├─── 1:N ─── 饮食记录 (meals_meal)
    │       ├── meal_type: 餐食类型
    │       ├── image: 食物图片
    │       └── calories: 卡路里
    │
    └─── 1:N ─── 睡眠记录 (sleep_sleeprecord)
            ├── sleep_time: 入睡时间
            ├── wake_time: 起床时间
            └── quality: 睡眠质量
```

## 四、存储位置详情

### 4.1 数据库存储
| 数据类型 | 存储位置 | 访问方式 |
|----------|----------|----------|
| 用户信息 | PostgreSQL `auth_user`表 | Django ORM: `User.objects` |
| 打卡记录 | PostgreSQL `checkin_checkin`表 | Django ORM: `Checkin.objects` |
| 饮食记录 | PostgreSQL `meals_meal`表 | Django ORM: `Meal.objects` |
| 睡眠记录 | PostgreSQL `sleep_sleeprecord`表 | Django ORM: `SleepRecord.objects` |
| 会话数据 | PostgreSQL `django_session`表 | Django Session框架 |
| 缓存数据 | Redis 内存数据库 | Django Cache框架 |

### 4.2 文件存储
| 文件类型 | 存储路径 | 配置 |
|----------|----------|------|
| 食物图片 | `media/meal_images/` | `MEDIA_ROOT = BASE_DIR / 'media'` |
| 静态文件 | `staticfiles/` | `STATIC_ROOT = BASE_DIR / 'staticfiles'` |
| 日志文件 | 系统日志目录 | Django logging配置 |
| SQLite数据库 | `db.sqlite3` | 开发环境使用 |

### 4.3 缓存存储
```python
# settings.py 中的Redis配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL', "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

**缓存用途**:
- 用户会话缓存
- 页面片段缓存
- 查询结果缓存
- 频繁访问的数据缓存

## 五、数据访问模式

### 5.1 主要查询模式
1. **用户相关查询** (最频繁)
   ```python
   # 获取用户的所有打卡记录
   Checkin.objects.filter(user=request.user).order_by('-date')
   
   # 获取用户今日饮食记录
   Meal.objects.filter(user=request.user, date=timezone.now().date())
   
   # 获取用户最近7天睡眠记录
   SleepRecord.objects.filter(
       user=request.user, 
       date__gte=timezone.now().date() - timedelta(days=7)
   )
   ```

2. **时间范围查询**
   ```python
   # 按月统计打卡次数
   Checkin.objects.filter(
       user=request.user,
       date__year=2024,
       date__month=3
   ).count()
   ```

3. **关联查询**
   ```python
   # 获取用户信息及关联记录
   user = User.objects.get(username='testuser')
   checkins = user.checkin_set.all()  # 反向查询
   meals = user.meal_set.all()
   ```

### 5.2 索引优化建议
1. **复合索引**:
   ```sql
   -- 打卡记录表
   CREATE INDEX idx_checkin_user_date ON checkin_checkin(user_id, date DESC);
   
   -- 饮食记录表  
   CREATE INDEX idx_meal_user_date_type ON meals_meal(user_id, date, meal_type);
   
   -- 睡眠记录表
   CREATE INDEX idx_sleep_user_date ON sleep_sleeprecord(user_id, date DESC);
   ```

2. **查询优化**:
   - 分页查询避免全表扫描
   - 使用`select_related`减少查询次数
   - 适当使用缓存减少数据库压力

## 六、数据安全与备份

### 6.1 数据安全
- **用户密码**: 使用Django的PBKDF2算法加密存储
- **敏感数据**: 环境变量配置数据库连接信息
- **文件权限**: 媒体文件目录权限控制
- **SQL注入防护**: Django ORM自动参数化查询

### 6.2 备份策略
1. **数据库备份**:
   ```bash
   # PostgreSQL备份
   pg_dump -U postgres ai_sport_db > backup_$(date +%Y%m%d).sql
   
   # SQLite备份
   cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3
   ```

2. **文件备份**:
   ```bash
   # 媒体文件备份
   tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
   
   # 静态文件备份
   tar -czf static_backup_$(date +%Y%m%d).tar.gz staticfiles/
   ```

3. **Docker数据卷备份**:
   ```bash
   # Docker Compose数据卷备份
   docker-compose exec db pg_dump -U postgres ai_sport_db > docker_backup.sql
   ```

## 七、性能考虑

### 7.1 数据量预估
| 数据表 | 预估记录数 | 年增长率 | 存储空间 |
|--------|------------|----------|----------|
| 用户表 | 1,000-10,000 | 20% | 10-100MB |
| 打卡记录 | 100,000-1,000,000 | 50% | 100MB-1GB |
| 饮食记录 | 50,000-500,000 | 40% | 1-10GB (含图片) |
| 睡眠记录 | 30,000-300,000 | 30% | 50-500MB |

### 7.2 性能优化
1. **数据库层面**:
   - 定期清理过期会话数据
   - 分区表设计（按时间分区）
   - 读写分离（主从复制）

2. **应用层面**:
   - 使用Django缓存框架
   - 异步任务处理图片上传
   - 分页查询大数据集

3. **架构层面**:
   - CDN加速静态资源
   - 对象存储服务（如COS）存储图片
   - 数据库连接池配置

## 八、扩展性设计

### 8.1 水平扩展
- **用户分片**: 按用户ID哈希分片
- **读写分离**: 主库写，从库读
- **缓存集群**: Redis集群分担缓存压力

### 8.2 数据迁移
- **零停机迁移**: 使用数据库复制工具
- **版本回滚**: 保留多个备份版本
- **数据校验**: 迁移后数据一致性检查

## 九、监控与维护

### 9.1 监控指标
- 数据库连接数
- 查询响应时间
- 缓存命中率
- 磁盘使用率
- 错误日志监控

### 9.2 维护任务
1. **日常维护**:
   - 数据库备份验证
   - 日志文件清理
   - 缓存数据刷新

2. **定期维护**:
   - 数据库索引重建
   - 统计信息更新
   - 数据归档（历史数据迁移）

## 十、总结

### 优势
1. **结构清晰**: 模块化设计，数据模型职责明确
2. **扩展性强**: 支持PostgreSQL和Redis，易于水平扩展
3. **安全性高**: 使用Django安全框架，密码加密存储
4. **维护方便**: 标准Django ORM，迁移工具完善

### 改进建议
1. **数据归档**: 添加历史数据归档机制
2. **监控告警**: 集成数据库监控告警系统
3. **备份自动化**: 实现自动化备份和恢复流程
4. **性能优化**: 根据实际使用情况优化索引和查询

### 技术栈
- **数据库**: PostgreSQL 16 (生产), SQLite3 (开发)
- **缓存**: Redis 7
- **框架**: Django 5.1.4
- **部署**: Docker + Nginx + Gunicorn
- **存储**: 本地文件系统 + 可选对象存储

---

**文档版本**: 1.0  
**更新日期**: 2026-03-24  
**适用环境**: 生产环境/开发环境  
**数据规模**: 中小型应用 (支持万级用户)