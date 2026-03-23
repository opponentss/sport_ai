from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Checkin
from .forms import CheckinForm


@login_required
def checkin_list(request):
    """显示用户的健身打卡记录列表
    
    Args:
        request: HTTP 请求对象
        
    Returns:
        HttpResponse: 渲染的打卡记录列表页面
    """
    checkins = Checkin.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'checkin/checkin_list.html', {'checkins': checkins})


@login_required
def checkin_create(request):
    """创建新的健身打卡记录
    
    Args:
        request: HTTP 请求对象
        
    Returns:
        HttpResponse: 渲染的创建打卡记录页面或重定向到打卡记录列表
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
    """更新现有的健身打卡记录
    
    Args:
        request: HTTP 请求对象
        pk: 打卡记录的主键
        
    Returns:
        HttpResponse: 渲染的更新打卡记录页面或重定向到打卡记录列表
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
    """删除健身打卡记录
    
    Args:
        request: HTTP 请求对象
        pk: 打卡记录的主键
        
    Returns:
        HttpResponse: 渲染的确认删除页面或重定向到打卡记录列表
    """
    checkin = get_object_or_404(Checkin, pk=pk, user=request.user)
    if request.method == 'POST':
        checkin.delete()
        return redirect('checkin_list')
    return render(request, 'checkin/checkin_confirm_delete.html', {'checkin': checkin})
