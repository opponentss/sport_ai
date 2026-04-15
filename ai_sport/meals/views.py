"""
餐饮管理模块视图函数

本模块包含餐饮管理模块的所有视图函数，处理用户请求并返回相应的页面。
用户必须登录才能访问这些功能，确保餐饮数据的隐私性。

主要功能：
- 查看餐饮记录列表
- 创建新的餐饮记录（支持拍照上传）
- 编辑现有的餐饮记录
- 删除餐饮记录
- 调用AI食物识别API识别食物（功能预留）

访问控制：
- 所有视图函数都需要用户登录，未登录用户会被重定向到登录页面
- 用户只能查看、编辑和删除自己的餐饮记录
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests
import os
from .models import Meal
from .forms import MealForm


def recognize_food(image_path):
    """
    调用食物识别API识别图片中的食物

    使用配置的DeepSeek API对餐食图片进行食物识别，
    返回识别出的食物名称、卡路里和数量信息。

    Args:
        image_path (str): 图片文件的完整路径

    Returns:
        dict: 包含食物识别结果的字典，格式如下：
            {
                "foods": [
                    {"name": "食物名称", "calories": 卡路里数值, "quantity": "数量描述"}
                ],
                "total_calories": 总卡路里数值
            }
        None: 如果API调用失败或发生异常
    """
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
    """
    餐饮记录列表视图

    显示当前用户的所有餐饮记录，按创建时间降序排列（最新在前）。
    用户只能看到自己的餐饮记录，确保数据隐私。

    Args:
        request: Django HTTP请求对象

    Returns:
        HttpResponse: 渲染餐饮记录列表模板
    """
    meals = Meal.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'meals/meal_list.html', {'meals': meals})


@login_required
def meal_create(request):
    """
    创建餐饮记录视图

    显示餐饮记录创建表单，支持图片上传。
    使用POST方法处理表单提交（包括文件和图片），GET方法显示空表单。
    创建成功后自动关联当前用户并重定向到列表页。

    Args:
        request: Django HTTP请求对象

    Returns:
        HttpResponse: GET请求时渲染餐饮表单模板
                     POST请求成功后重定向到餐饮列表页
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
    """
    更新餐饮记录视图

    显示餐饮记录编辑表单，预填充现有数据，支持修改图片。
    使用POST方法处理表单提交（包括文件和图片），GET方法显示预填充的表单。
    用户只能编辑自己的餐饮记录。

    Args:
        request: Django HTTP请求对象
        pk: int，餐饮记录的主键ID

    Returns:
        HttpResponse: GET请求时渲染餐饮编辑表单模板（预填充现有数据）
                     POST请求成功后重定向到餐饮列表页
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
    """
    删除餐饮记录视图

    显示删除确认页面，用户确认后删除餐饮记录。
    使用POST方法处理删除操作，防止GET请求误删。
    用户只能删除自己的餐饮记录。

    Args:
        request: Django HTTP请求对象
        pk: int，餐饮记录的主键ID

    Returns:
        HttpResponse: GET请求时渲染删除确认模板
                     POST请求成功后重定向到餐饮列表页
    """
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        meal.delete()
        return redirect('meal_list')
    return render(request, 'meals/meal_confirm_delete.html', {'meal': meal})