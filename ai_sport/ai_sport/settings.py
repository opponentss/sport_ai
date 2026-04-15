"""
Django 项目配置文件

本文件包含 Django 项目的所有配置设置，包括数据库、静态文件、应用注册等。
配置分为多个部分，从基础路径设置到第三方服务集成。

配置优先级：
1. 环境变量（生产环境）
2. 默认值（开发环境）

主要配置模块：
- 基础设置（SECRET_KEY, DEBUG, ALLOWED_HOSTS）
- 应用定义（INSTALLED_APPS）
- 中间件配置（MIDDLEWARE）
- 模板配置（TEMPLATES）
- 数据库配置（DATABASES）
- 缓存配置（CACHES）
- 静态文件和媒体文件
- 第三方服务（食物识别API）
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-malu0x^bcos%-6et_s4978lcl5^fr%q5ll3l9i%9)9)h9)7_uc')

DEBUG = True

default_hosts = 'localhost,127.0.0.1,testserver'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', default_hosts).split(',')


INSTALLED_APPS = [
    'django.contrib.admin',         # Django 管理后台
    'django.contrib.auth',         # 用户认证系统
    'django.contrib.contenttypes', # 内容类型框架
    'django.contrib.sessions',    # 会话管理
    'django.contrib.messages',    # 消息框架
    'django.contrib.staticfiles', # 静态文件管理
    'checkin',                     # 运动打卡模块
    'meals',                       # 餐饮管理模块
    'sleep',                       # 睡眠记录模块
    'fitness_guide',               # 健身指南模块
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 安全中间件
    'django.contrib.sessions.middleware.SessionMiddleware',  # 会话中间件
    'django.middleware.common.CommonMiddleware',     # 通用中间件
    'django.middleware.csrf.CsrfViewMiddleware',    # CSRF 防护
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 认证中间件
    'django.contrib.messages.middleware.MessageMiddleware',  # 消息中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 点击劫持防护
]

ROOT_URLCONF = 'ai_sport.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'ai_sport' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',     # 调试信息
                'django.template.context_processors.request',   # 请求对象
                'django.contrib.auth.context_processors.auth', # 认证用户
                'django.contrib.messages.context_processors.messages',  # 消息
            ],
        },
    },
]

WSGI_APPLICATION = 'ai_sport.wsgi.application'


import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # 用户属性相似度
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # 最小长度验证
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # 常用密码验证
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # 数字密码验证
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', BASE_DIR / 'staticfiles')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', BASE_DIR / 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL', "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


FOOD_RECOGNITION_API_URL = "https://api.deepseek.com"
FOOD_RECOGNITION_API_KEY = "sk-04916ae563d8479fbfc857d0c49e7b51"


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'