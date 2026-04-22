"""
Django 项目主 URL 配置

本模块定义了项目的所有 URL 路由规则，将 URL 路径映射到对应的视图函数。
采用分布式 URL 配置，各应用模块管理自己的 URL，通过 include() 整合到主路由。

路由结构概览：
- /              → 项目首页
- /admin/        → Django 管理后台
- /checkin/      → 运动打卡模块
- /meals/        → 餐饮管理模块
- /sleep/        → 睡眠记录模块
- /fitness-guide/ → 健身指南模块
- /accounts/      → 用户认证相关页面（登录、登出、注册）

开发环境：
- DEBUG 模式下支持静态文件和媒体文件访问
- 使用 Django 内置开发服务器

生产环境：
- 应使用 Nginx 提供静态文件和媒体文件服务
- 应使用 Gunicorn 或 uWSGI 作为 WSGI 应用服务器
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from . import views


def home(request):
    """
    项目首页视图

    渲染项目首页模板，显示欢迎信息和主要功能入口。
    作为整个应用的主入口页面。

    Args:
        request: Django HTTP请求对象

    Returns:
        HttpResponse: 渲染的首页模板
    """
    return render(request, 'home.html')


urlpatterns = [
    # 项目首页
    path('', home, name='home'),

    # Django 管理后台
    path('admin/', admin.site.urls),

    # 运动打卡模块路由
    # 包含：打卡列表、创建打卡、编辑打卡、删除打卡
    path('checkin/', include('checkin.urls')),

    # 餐饮管理模块路由
    # 包含：餐饮列表、创建餐饮、编辑餐饮、删除餐饮
    path('meals/', include('meals.urls')),

    # 睡眠记录模块路由
    # 包含：睡眠记录列表、创建记录、编辑记录、删除记录
    path('sleep/', include('sleep.urls')),

    # 健身指南模块路由
    # 包含：健身指南首页、饮食建议、肌肉认识、器材认识
    path('fitness-guide/', include('fitness_guide.urls')),

    # 用户认证路由
    # 登录页面：使用 Django 内置认证视图，指定登录模板
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # 登出页面：使用 Django 内置认证视图，登出后返回首页
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # 用户注册页面：使用自定义视图处理
    path('accounts/register/', views.register, name='register'),

    # 用户个人中心
    path('profile/', views.user_profile, name='user_profile'),
]


if settings.DEBUG:
    # 开发环境下提供媒体文件访问服务
    # 生产环境应使用 Nginx 等 web 服务器提供这些文件
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)