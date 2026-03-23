from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SleepRecord
from .forms import SleepRecordForm


@login_required
def sleep_list(request):
    """显示用户的睡眠记录列表
    
    Args:
        request: HTTP 请求对象
        
    Returns:
        HttpResponse: 渲染的睡眠记录列表页面
    """
    sleep_records = SleepRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, 'sleep/sleep_list.html', {'sleep_records': sleep_records})


@login_required
def sleep_create(request):
    """创建新的睡眠记录
    Args:
        request: HTTP 请求对象
        
    Returns:
        HttpResponse: 渲染的创建睡眠记录页面或重定向到睡眠记录列表
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
    """更新现有的睡眠记录
    
    Args:
        request: HTTP 请求对象
        pk: 睡眠记录的主键
        
    Returns:
        HttpResponse: 渲染的更新睡眠记录页面或重定向到睡眠记录列表
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
    """删除睡眠记录
    
    Args:
        request: HTTP 请求对象
        pk: 睡眠记录的主键
        
    Returns:
        HttpResponse: 渲染的确认删除页面或重定向到睡眠记录列表
    """
    sleep_record = get_object_or_404(SleepRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        sleep_record.delete()
        return redirect('sleep_list')
    return render(request, 'sleep/sleep_confirm_delete.html', {'sleep_record': sleep_record})
