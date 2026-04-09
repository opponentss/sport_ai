from django.shortcuts import render

def fitness_guide_home(request):
    """健身前你该知道的主页面"""
    context = {
        'title': '健身前你该知道的',
        'description': '了解健身基础知识，为你的健身之旅做好准备',
        'modules': [
            {'name': '饮食建议', 'url': 'diet_advice', 'description': '了解健身前后的饮食原则和营养搭配'},
            {'name': '肌肉认识', 'url': 'muscle_knowledge', 'description': '认识主要肌肉群及其功能，科学训练'},
            {'name': '器材认识', 'url': 'equipment_knowledge', 'description': '熟悉健身房常见器材的使用方法'},
        ]
    }
    return render(request, 'fitness_guide/home.html', context)

def diet_advice(request):
    """饮食建议页面"""
    context = {
        'title': '饮食建议',
        'sections': [
            {
                'title': '健身前饮食',
                'content': '健身前1-2小时应摄入易消化的碳水化合物和少量蛋白质，如香蕉、全麦面包等。避免高脂肪食物，以免影响消化。'
            },
            {
                'title': '健身后饮食',
                'content': '健身后30分钟内是补充营养的黄金窗口，应摄入优质蛋白质和快速吸收的碳水化合物，帮助肌肉恢复和生长。'
            },
            {
                'title': '日常营养搭配',
                'content': '保持均衡饮食，蛋白质、碳水化合物和健康脂肪的比例建议为3:4:3。多摄入蔬菜水果，补充维生素和矿物质。'
            }
        ]
    }
    return render(request, 'fitness_guide/detail.html', context)

def muscle_knowledge(request):
    """肌肉认识页面"""
    context = {
        'title': '肌肉认识',
        'sections': [
            {
                'title': '胸肌 (Pectoralis)',
                'content': '包括胸大肌和胸小肌，主要负责手臂的内收和屈曲。常见训练动作：卧推、俯卧撑、飞鸟。'
            },
            {
                'title': '背肌 (Back Muscles)',
                'content': '包括背阔肌、斜方肌等，主要负责肩关节的后伸和内收。常见训练动作：引体向上、划船、硬拉。'
            },
            {
                'title': '腿部肌肉 (Leg Muscles)',
                'content': '包括股四头肌、腘绳肌、小腿肌群等，负责行走、跑步和跳跃。常见训练动作：深蹲、腿举、腿弯举。'
            }
        ]
    }
    return render(request, 'fitness_guide/detail.html', context)

def equipment_knowledge(request):
    """器材认识页面"""
    context = {
        'title': '器材认识',
        'sections': [
            {
                'title': '有氧器材',
                'content': '跑步机、椭圆机、动感单车等，主要用于提高心肺功能和燃烧脂肪。使用时注意姿势正确，避免关节损伤。'
            },
            {
                'title': '力量训练器材',
                'content': '包括杠铃、哑铃、史密斯机、龙门架等，用于增强肌肉力量和耐力。初学者应从轻重量开始，掌握正确动作。'
            },
            {
                'title': '功能性训练器材',
                'content': 'TRX悬挂训练带、壶铃、战绳等，用于提高身体协调性、平衡性和核心力量。适合有一定基础的人群。'
            }
        ]
    }
    return render(request, 'fitness_guide/detail.html', context)
