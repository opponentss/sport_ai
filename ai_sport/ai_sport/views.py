"""
ai_sport 项目视图
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkin.models import Checkin
from meals.models import Meal
from sleep.models import SleepRecord
from user_profile.models import UserProfile


def register(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # 自动登录新用户
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'注册成功！欢迎 {username}！')
                return redirect('home')
        else:
            # 显示表单错误
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def user_profile(request):
    """用户个人中心视图"""
    user = request.user
    
    # 获取或创建用户资料
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST' and request.FILES.get('avatar'):
        # 处理头像上传
        avatar_file = request.FILES['avatar']
        
        # 验证文件类型
        if avatar_file.content_type.startswith('image/'):
            profile.avatar = avatar_file
            profile.save()
            messages.success(request, '头像更新成功！')
        else:
            messages.error(request, '请上传图片文件！')
        
        return redirect('user_profile')
    
    # 统计用户数据
    checkin_count = Checkin.objects.filter(user=user).count()
    meal_count = Meal.objects.filter(user=user).count()
    sleep_count = SleepRecord.objects.filter(user=user).count()
    
    # 获取最近的记录
    recent_checkins = Checkin.objects.filter(user=user).order_by('-date', '-time')[:5]
    recent_meals = Meal.objects.filter(user=user).order_by('-date', '-time')[:5]
    recent_sleeps = SleepRecord.objects.filter(user=user).order_by('-date')[:5]
    
    context = {
        'user': user,
        'profile': profile,
        'checkin_count': checkin_count,
        'meal_count': meal_count,
        'sleep_count': sleep_count,
        'recent_checkins': recent_checkins,
        'recent_meals': recent_meals,
        'recent_sleeps': recent_sleeps,
    }
    
    return render(request, 'user_profile/profile.html', context)