"""
餐饮管理模块视图函数

本模块包含餐饮管理模块的所有视图函数，处理用户请求并返回相应的页面。
用户必须登录才能访问这些功能，确保餐饮数据的隐私性。

主要功能：
- 查看餐饮记录列表
- 创建新的餐饮记录（支持拍照上传）
- 编辑现有的餐饮记录
- 删除餐饮记录
- 调用AI食物识别API识别食物
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests
import base64
import json
import re
from .models import Meal
from .forms import MealForm


@csrf_exempt
@login_required
def analyze_food(request):
    """
    AI 食物识别分析 API 端点

    接收上传的食物图片，使用 DeepSeek API 进行食物识别和营养分析。
    返回识别出的食物列表、总卡路里和营养建议。

    请求方法：POST
    请求参数：
        - image: 图片文件（通过表单上传）
        - image_base64: base64 编码的图片数据（可选）

    返回格式：
        {
            "success": true/false,
            "foods": [
                {"name": "食物名称", "calories": 数值, "quantity": "份量描述"}
            ],
            "total_calories": 总卡路里,
            "nutrition_tips": "营养建议",
            "description": "综合描述"
        }
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '只支持 POST 请求'})

    try:
        image_data = None

        if 'image' in request.FILES:
            image_file = request.FILES['image']
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        elif 'image_base64' in request.POST:
            image_data = request.POST['image_base64']
            if ',' in image_data:
                image_data = image_data.split(',')[1]

        if not image_data:
            return JsonResponse({'success': False, 'error': '未提供图片数据'})

        prompt = """你是一个专业的食物营养分析AI。请分析这张图片中的食物，并返回JSON格式的营养分析结果。

请严格按照以下JSON格式返回，不要添加任何其他内容：
{
    "foods": [
        {"name": "食物名称", "calories": 数值, "quantity": "份量描述"}
    ],
    "total_calories": 总卡路里数值,
    "nutrition_tips": "简短营养建议（20字以内）",
    "description": "整体食物描述（30字以内）"
}

注意事项：
- 只识别你确定是食物的内容
- 卡路里数值使用整数
- 如果无法识别，返回空数组和0卡路里
- 确保JSON格式完全正确，可以被解析"""

        api_url = "https://api.deepseek.com/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.FOOD_RECOGNITION_API_KEY}'
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }

        response = requests.post(api_url, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            return JsonResponse({
                'success': False,
                'error': f'API 请求失败: {response.status_code}'
            })

        result = response.json()
        content = result.get('choices', [{}])[0].get('message', {}).get('content', '')

        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            analysis_result = json.loads(json_match.group())
            return JsonResponse({
                'success': True,
                'foods': analysis_result.get('foods', []),
                'total_calories': analysis_result.get('total_calories', 0),
                'nutrition_tips': analysis_result.get('nutrition_tips', ''),
                'description': analysis_result.get('description', '')
            })
        else:
            return JsonResponse({
                'success': False,
                'error': '无法解析识别结果，请重试'
            })

    except requests.exceptions.Timeout:
        return JsonResponse({'success': False, 'error': '请求超时，请重试'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def recognize_food(image_path):
    """
    调用食物识别API识别图片中的食物

    使用配置的DeepSeek API对餐食图片进行食物识别，
    返回识别出的食物名称、卡路里和数量信息。
      
    Args:
        image_path (str): 图片文件的完整路径

    Returns:
        dict: 包含食物识别结果的字典
        None: 如果API调用失败或发生异常
    """

    try:
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        prompt = """分析这张食物图片，返回JSON格式：
        {"foods": [{"name": "名称", "calories": 数值, "quantity": "份量"}], "total_calories": 数值}"""

        api_url = "https://api.deepseek.com/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.FOOD_RECOGNITION_API_KEY}'
        }


        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            import json as json_module
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                return json_module.loads(json_match.group())
        return None
    except Exception as e:
        print(f"Error recognizing food: {e}")
        return None


@login_required
def meal_list(request):
    """餐饮记录列表视图"""
    meals = Meal.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'meals/meal_list.html', {'meals': meals})


@login_required
def meal_create(request):
    """创建餐饮记录视图"""
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
    """更新餐饮记录视图"""
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
    """删除餐饮记录视图"""
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        meal.delete()
        return redirect('meal_list')
    return render(request, 'meals/meal_confirm_delete.html', {'meal': meal})

