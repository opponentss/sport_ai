"""
健身指南模块视图函数

本模块包含健身指南模块的所有视图函数，处理用户请求并返回相应的页面。
包括健身指南首页、饮食建议、肌肉认识、器材认识等功能。

主要功能：
- 健身指南首页：展示三大模块入口
- 饮食建议：支持管理员添加内容
- 肌肉认识：支持管理员添加肌肉群和部位
- 器材认识：支持图片和视频
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from .models import Equipment, DietItem, MuscleGroup, MuscleItem


def fitness_guide_home(request):
    """健身指南模块首页"""
    context = {
        'title': '健身前你该知道的',
        'description': '了解健身基础知识，为你的健身之旅做好准备',
        'modules': [
            {'name': '饮食建议', 'url': 'diet_home', 'description': '了解健身前后的饮食原则和营养搭配'},
            {'name': '肌肉认识', 'url': 'muscle_home', 'description': '认识主要肌肉群及其功能，科学训练'},
            {'name': '器材认识', 'url': 'equipment_knowledge', 'description': '熟悉健身房常见器材的使用方法'},
        ]
    }
    return render(request, 'fitness_guide/home.html', context)


# ==================== 饮食建议视图 ====================

def diet_home(request):
    """饮食建议首页"""
    categories = [
        {'key': 'pre_workout', 'name': '健身前饮食', 'description': '运动前的饮食准备，选择合适的食物和时间，为运动提供能量支持。'},
        {'key': 'post_workout', 'name': '健身后饮食', 'description': '运动后的营养补充，抓住黄金窗口期，促进肌肉恢复和生长。'},
        {'key': 'daily_nutrition', 'name': '日常营养', 'description': '均衡饮食指南，了解蛋白质、碳水化合物、脂肪的正确搭配。'},
        {'key': 'supplement', 'name': '营养补剂', 'description': '科学使用营养补剂，蛋白粉、支链氨基酸等补剂的正确服用方法。'},
        {'key': 'tips', 'name': '饮食小贴士', 'description': '实用的饮食技巧和建议，帮助你养成健康的饮食习惯。'}
    ]
    featured_items = DietItem.objects.filter(is_featured=True)[:3]
    context = {
        'title': '饮食建议',
        'categories': categories,
        'featured_items': featured_items,
    }
    return render(request, 'fitness_guide/diet_home.html', context)


def diet_list(request, category):
    """按类别显示饮食建议列表"""
    category_names = {
        'pre_workout': '健身前饮食', 'post_workout': '健身后饮食',
        'daily_nutrition': '日常营养', 'supplement': '营养补剂', 'tips': '饮食小贴士',
    }
    diet_items = DietItem.objects.filter(category=category)
    context = {
        'title': category_names.get(category, '饮食建议'),
        'category': category,
        'diet_items': diet_items,
    }
    return render(request, 'fitness_guide/diet_list.html', context)


def diet_detail(request, category, diet_id):
    """饮食建议详情页"""
    diet_item = get_object_or_404(DietItem, id=diet_id, category=category)
    context = {'diet_item': diet_item}
    return render(request, 'fitness_guide/diet_detail.html', context)


@staff_member_required
def diet_create(request, category):
    """添加饮食建议"""
    category_names = {
        'pre_workout': '健身前饮食', 'post_workout': '健身后饮食',
        'daily_nutrition': '日常营养', 'supplement': '营养补剂', 'tips': '饮食小贴士',
    }
    if request.method == 'POST':
        from .forms import DietItemForm
        form = DietItemForm(request.POST, request.FILES)
        if form.is_valid():
            diet_item = form.save(commit=False)
            diet_item.category = category
            diet_item.save()
            return redirect('diet_list', category=category)
    else:
        form = DietItemForm(initial={'category': category})
    context = {
        'title': f'添加{category_names.get(category, "饮食建议")}',
        'form': form, 'category': category,
    }
    return render(request, 'fitness_guide/diet_form.html', context)


@staff_member_required
def diet_update(request, category, diet_id):
    """编辑饮食建议"""
    diet_item = get_object_or_404(DietItem, id=diet_id, category=category)
    if request.method == 'POST':
        from .forms import DietItemForm
        form = DietItemForm(request.POST, request.FILES, instance=diet_item)
        if form.is_valid():
            form.save()
            return redirect('diet_detail', category=category, diet_id=diet_id)
    else:
        form = DietItemForm(instance=diet_item)
    context = {
        'title': f'编辑饮食建议 - {diet_item.title}',
        'form': form, 'diet_item': diet_item, 'category': category,
    }
    return render(request, 'fitness_guide/diet_form.html', context)


@staff_member_required
def diet_delete(request, category, diet_id):
    """删除饮食建议"""
    diet_item = get_object_or_404(DietItem, id=diet_id, category=category)
    if request.method == 'POST':
        diet_item.delete()
        return redirect('diet_list', category=category)
    context = {
        'title': f'删除饮食建议 - {diet_item.title}',
        'diet_item': diet_item, 'category': category,
    }
    return render(request, 'fitness_guide/diet_confirm_delete.html', context)


# ==================== 肌肉认识视图 ====================

def muscle_home(request):
    """肌肉认识首页"""
    muscle_groups = MuscleGroup.objects.all()

    # 按大类分组
    grouped = {}
    for group in muscle_groups:
        cat = group.category
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(group)

    # 获取推荐的肌肉部位
    featured_items = MuscleItem.objects.filter(is_featured=True)[:4]

    category_info = {
        'upper': {'name': '上肢肌群', 'icon': '💪'},
        'core': {'name': '核心肌群', 'icon': '🎯'},
        'lower': {'name': '下肢肌群', 'icon': '🦵'},
        'cardio': {'name': '心肺功能', 'icon': '❤️'},
    }

    context = {
        'title': '肌肉认识',
        'grouped_muscle_groups': grouped,
        'featured_items': featured_items,
        'category_info': category_info,
    }
    return render(request, 'fitness_guide/muscle_home.html', context)


def muscle_group_list(request, group_id):
    """显示特定肌肉群下的所有肌肉部位"""
    muscle_group = get_object_or_404(MuscleGroup, id=group_id)
    muscle_items = MuscleItem.objects.filter(muscle_group=muscle_group)
    context = {
        'muscle_group': muscle_group,
        'muscle_items': muscle_items,
    }
    return render(request, 'fitness_guide/muscle_list.html', context)


def muscle_detail(request, group_id, muscle_id):
    """肌肉部位详情页"""
    muscle_item = get_object_or_404(MuscleItem, id=muscle_id, muscle_group_id=group_id)
    context = {'muscle_item': muscle_item}
    return render(request, 'fitness_guide/muscle_detail.html', context)


@staff_member_required
def muscle_group_create(request):
    """添加肌肉群"""
    if request.method == 'POST':
        from .forms import MuscleGroupForm
        form = MuscleGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('muscle_home')
    else:
        form = MuscleGroupForm()
    context = {'title': '添加肌肉群', 'form': form}
    return render(request, 'fitness_guide/muscle_group_form.html', context)


@staff_member_required
def muscle_item_create(request, group_id):
    """添加肌肉部位"""
    muscle_group = get_object_or_404(MuscleGroup, id=group_id)
    if request.method == 'POST':
        from .forms import MuscleItemForm
        form = MuscleItemForm(request.POST, request.FILES)
        if form.is_valid():
            muscle_item = form.save(commit=False)
            muscle_item.muscle_group = muscle_group
            muscle_item.save()
            return redirect('muscle_group_list', group_id=group_id)
    else:
        form = MuscleItemForm(initial={'muscle_group': muscle_group})
    context = {
        'title': f'添加{muscle_group.name}部位的肌肉',
        'form': form,
        'muscle_group': muscle_group,
    }
    return render(request, 'fitness_guide/muscle_item_form.html', context)


@staff_member_required
def muscle_item_update(request, group_id, muscle_id):
    """编辑肌肉部位"""
    muscle_item = get_object_or_404(MuscleItem, id=muscle_id, muscle_group_id=group_id)
    if request.method == 'POST':
        from .forms import MuscleItemForm
        form = MuscleItemForm(request.POST, request.FILES, instance=muscle_item)
        if form.is_valid():
            form.save()
            return redirect('muscle_detail', group_id=group_id, muscle_id=muscle_id)
    else:
        form = MuscleItemForm(instance=muscle_item)
    context = {
        'title': f'编辑 - {muscle_item.name}',
        'form': form,
        'muscle_item': muscle_item,
    }
    return render(request, 'fitness_guide/muscle_item_form.html', context)


@staff_member_required
def muscle_item_delete(request, group_id, muscle_id):
    """删除肌肉部位"""
    muscle_item = get_object_or_404(MuscleItem, id=muscle_id, muscle_group_id=group_id)
    if request.method == 'POST':
        muscle_item.delete()
        return redirect('muscle_group_list', group_id=group_id)
    context = {
        'title': f'删除 - {muscle_item.name}',
        'muscle_item': muscle_item,
    }
    return render(request, 'fitness_guide/muscle_confirm_delete.html', context)


# ==================== 器材认识视图 ====================

def equipment_knowledge(request):
    """器材认识首页"""
    categories = [
        {'key': 'cardio', 'name': '有氧器材', 'description': '跑步机、椭圆机、动感单车等，主要用于提高心肺功能和燃烧脂肪。'},
        {'key': 'strength', 'name': '力量训练器材', 'description': '包括杠铃、哑铃、史密斯机、龙门架等，用于增强肌肉力量和耐力。'},
        {'key': 'functional', 'name': '功能性训练器材', 'description': 'TRX悬挂训练带、壶铃、战绳等，用于提高身体协调性、平衡性和核心力量。'}
    ]
    context = {'title': '器材认识', 'categories': categories}
    return render(request, 'fitness_guide/equipment_home.html', context)


def equipment_list(request, category):
    """按类别显示器材列表"""
    category_names = {
        'cardio': '有氧器材', 'strength': '力量训练器材', 'functional': '功能性训练器材'
    }
    equipment_list = Equipment.objects.filter(category=category)
    context = {
        'title': category_names.get(category, '器材列表'),
        'category': category,
        'equipment_list': equipment_list,
    }
    return render(request, 'fitness_guide/equipment_list.html', context)


def equipment_detail(request, category, equipment_id):
    """器材详情页"""
    equipment = get_object_or_404(Equipment, id=equipment_id, category=category)
    context = {'equipment': equipment}
    return render(request, 'fitness_guide/equipment_detail.html', context)


@staff_member_required
def equipment_create(request, category):
    """添加器材"""
    category_names = {
        'cardio': '有氧器材', 'strength': '力量训练器材', 'functional': '功能性训练器材'
    }
    if request.method == 'POST':
        from .forms import EquipmentForm
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.category = category
            equipment.save()
            return redirect('equipment_list', category=category)
    else:
        form = EquipmentForm(initial={'category': category})
    context = {
        'title': f'添加{category_names.get(category, "器材")}',
        'form': form, 'category': category,
    }
    return render(request, 'fitness_guide/equipment_form.html', context)


@staff_member_required
def equipment_update(request, category, equipment_id):
    """编辑器材"""
    equipment = get_object_or_404(Equipment, id=equipment_id, category=category)
    if request.method == 'POST':
        from .forms import EquipmentForm
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment_detail', category=category, equipment_id=equipment_id)
    else:
        form = EquipmentForm(instance=equipment)
    context = {
        'title': f'编辑器材 - {equipment.name}',
        'form': form, 'equipment': equipment, 'category': category,
    }
    return render(request, 'fitness_guide/equipment_form.html', context)


@staff_member_required
def equipment_delete(request, category, equipment_id):
    """删除器材"""
    equipment = get_object_or_404(Equipment, id=equipment_id, category=category)
    if request.method == 'POST':
        equipment.delete()
        return redirect('equipment_list', category=category)
    context = {
        'title': f'删除器材 - {equipment.name}',
        'equipment': equipment, 'category': category,
    }
    return render(request, 'fitness_guide/equipment_confirm_delete.html', context)