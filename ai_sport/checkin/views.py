"""
运动打卡模块视图函数

本模块包含运动打卡模块的所有视图函数，处理用户请求并返回相应的页面。
用户必须登录才能访问这些功能，确保运动打卡数据的隐私性。

主要功能：
- 查看打卡记录列表
- 创建新的打卡记录
- 编辑现有的打卡记录
- 删除打卡记录

访问控制：
- 所有视图函数都需要用户登录，未登录用户会被重定向到登录页面
- 用户只能查看、编辑和删除自己的打卡记录
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Checkin
from .forms import CheckinForm


@login_required
def checkin_list(request):
    """
    打卡记录列表视图

    显示当前用户的所有运动打卡记录，按创建时间降序排列（最新在前）。
    用户只能看到自己的打卡记录，确保数据隐私。

    Args:
        request: Django HTTP请求对象

    Returns:
        HttpResponse: 渲染打卡记录列表模板
    """
    checkins = Checkin.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'checkin/checkin_list.html', {'checkins': checkins})


@login_required
def checkin_create(request):
    """
    创建打卡记录视图

    显示打卡记录创建表单，处理表单提交以创建新的打卡记录。
    使用POST方法处理表单提交，GET方法显示空表单。
    创建成功后自动关联当前用户并重定向到列表页。

    Args:
        request: Django HTTP请求对象

    Returns:
        HttpResponse: GET请求时渲染打卡表单模板
                     POST请求成功后重定向到打卡列表页
    """
    if request.method == 'POST':
        form = CheckinForm(request.POST)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.user = request.user
            checkin.save()
            return redirect('checkin_list')
    else:
        form = CheckinForm()
    return render(request, 'checkin/checkin_form.html', {'form': form})


@login_required
def checkin_update(request, pk):
    """
    更新打卡记录视图

    显示打卡记录编辑表单，预填充现有数据。
    使用POST方法处理表单提交，GET方法显示预填充的表单。
    用户只能编辑自己的打卡记录。

    Args:
        request: Django HTTP请求对象
        pk: int，打卡记录的主键ID

    Returns:
        HttpResponse: GET请求时渲染打卡编辑表单模板（预填充现有数据）
                     POST请求成功后重定向到打卡列表页
    """
    checkin = get_object_or_404(Checkin, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CheckinForm(request.POST, instance=checkin)
        if form.is_valid():
            form.save()
            return redirect('checkin_list')
    else:
        form = CheckinForm(instance=checkin)
    return render(request, 'checkin/checkin_form.html', {'form': form})


@login_required
def checkin_delete(request, pk):
    """
    删除打卡记录视图

    显示删除确认页面，用户确认后删除打卡记录。
    使用POST方法处理删除操作，防止GET请求误删。
    用户只能删除自己的打卡记录。

    Args:
        request: Django HTTP请求对象
        pk: int，打卡记录的主键ID

    Returns:
        HttpResponse: GET请求时渲染删除确认模板
                     POST请求成功后重定向到打卡列表页
    """
    checkin = get_object_or_404(Checkin, pk=pk, user=request.user)
    if request.method == 'POST':
        checkin.delete()
        return redirect('checkin_list')
    return render(request, 'checkin/checkin_confirm_delete.html', {'checkin': checkin})