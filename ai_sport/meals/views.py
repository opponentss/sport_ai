from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests
import os
from .models import Meal
from .forms import MealForm


def recognize_food(image_path):
    """调用食物识别 API 识别图片中的食物
    
    Args:
        image_path (str): 图片文件路径
        
    Returns:
        dict: 包含食物识别结果的字典，格式如下：
            {
                "foods": [
                    {"name": "食物名称", "calories": 卡路里, "quantity": "数量"}
                ],
                "total_calories": 总卡路里
            }
        None: 如果识别失败
    """
    # 实际 API 调用示例
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            headers = {'Authorization': f'Bearer {settings.FOOD_RECOGNITION_API_KEY}'}
            response = requests.post(settings.FOOD_RECOGNITION_API_URL, files=files, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return None
    except Exception as e:
        print(f"Error recognizing food: {e}")
        return None


@login_required
def meal_list(request):
    """显示用户的三餐记录列表
    
    Args:
        request: HTTP 请求对象
        
    Returns:
        HttpResponse: 渲染的餐食列表页面
    """
    meals = Meal.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'meals/meal_list.html', {'meals': meals})


@login_required
def meal_create(request):
    """创建新的三餐记录
    
    Args:
        request: HTTP 请求对象
        
    Returns:
        HttpResponse: 渲染的创建餐食页面或重定向到餐食列表
    """
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect('meal_list')
    else:
        form = MealForm()
    return render(request, 'meals/meal_form.html', {'form': form})


@login_required
def meal_update(request, pk):
    """更新现有的三餐记录
    
    Args:
        request: HTTP 请求对象
        pk: 餐食记录的主键
        
    Returns:
        HttpResponse: 渲染的更新餐食页面或重定向到餐食列表
    """
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('meal_list')
    else:
        form = MealForm(instance=meal)
    return render(request, 'meals/meal_form.html', {'form': form})


@login_required
def meal_delete(request, pk):
    """删除三餐记录
    
    Args:
        request: HTTP 请求对象
        pk: 餐食记录的主键
        
    Returns:
        HttpResponse: 渲染的确认删除页面或重定向到餐食列表
    """
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        meal.delete()
        return redirect('meal_list')
    return render(request, 'meals/meal_confirm_delete.html', {'meal': meal})
