"""
睡眠记录模块视图函数

本模块包含睡眠记录模块的所有视图函数，处理用户请求并返回相应的页面。
用户必须登录才能访问这些功能，确保睡眠数据的隐私性。

主要功能：
- 查看睡眠记录列表
- 创建新的睡眠记录
- 编辑现有的睡眠记录
- 删除睡眠记录

访问控制：
- 所有视图函数都需要用户登录，未登录用户会被重定向到登录页面
- 用户只能查看、编辑和删除自己的睡眠记录
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SleepRecord
from .forms import SleepRecordForm


@login_required
def sleep_list(request):
    """
    睡眠记录列表视图

    显示当前用户的所有睡眠记录，按日期降序排列（最新在前）。
    用户只能看到自己的睡眠记录，确保数据隐私。

    Args:
        request: Django HTTP请求对象

    Returns:
        HttpResponse: 渲染睡眠记录列表模板
    """
    sleep_records = SleepRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, 'sleep/sleep_list.html', {'sleep_records': sleep_records})


@login_required
def sleep_create(request):
    """
    创建睡眠记录视图

    显示睡眠记录创建表单，处理表单提交以创建新的睡眠记录。
    使用POST方法处理表单提交，GET方法显示空表单。
    创建成功后自动关联当前用户并重定向到列表页。

    Args:
        request: Django HTTP请求对象

    Returns:
        HttpResponse: GET请求时渲染睡眠表单模板
                     POST请求成功后重定向到睡眠列表页
    """
    if request.method == 'POST':
        form = SleepRecordForm(request.POST)
        if form.is_valid():
            sleep_record = form.save(commit=False)
            sleep_record.user = request.user
            sleep_record.save()
            return redirect('sleep_list')
    else:
        form = SleepRecordForm()
    return render(request, 'sleep/sleep_form.html', {'form': form})


@login_required
def sleep_update(request, pk):
    """
    更新睡眠记录视图

    显示睡眠记录编辑表单，预填充现有数据。
    使用POST方法处理表单提交，GET方法显示预填充的表单。
    用户只能编辑自己的睡眠记录。

    Args:
        request: Django HTTP请求对象
        pk: int，睡眠记录的主键ID

    Returns:
        HttpResponse: GET请求时渲染睡眠编辑表单模板（预填充现有数据）
                     POST请求成功后重定向到睡眠列表页
    """
    sleep_record = get_object_or_404(SleepRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SleepRecordForm(request.POST, instance=sleep_record)
        if form.is_valid():
            form.save()
            return redirect('sleep_list')
    else:
        form = SleepRecordForm(instance=sleep_record)
    return render(request, 'sleep/sleep_form.html', {'form': form})


@login_required
def sleep_delete(request, pk):
    """
    删除睡眠记录视图

    显示删除确认页面，用户确认后删除睡眠记录。
    使用POST方法处理删除操作，防止GET请求误删。
    用户只能删除自己的睡眠记录。

    Args:
        request: Django HTTP请求对象
        pk: int，睡眠记录的主键ID

    Returns:
        HttpResponse: GET请求时渲染删除确认模板
                     POST请求成功后重定向到睡眠列表页
    """
    sleep_record = get_object_or_404(SleepRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        sleep_record.delete()
        return redirect('sleep_list')
    return render(request, 'sleep/sleep_confirm_delete.html', {'sleep_record': sleep_record})