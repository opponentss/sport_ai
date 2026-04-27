from .models import TrainingPlan, TrainingExercise, Achievement
from django.utils import timezone


def seed_training_plans():
    plans_data = [
        {
            'name': '晨间唤醒',
            'description': '轻柔的拉伸动作，慢慢唤醒身体，不跳不吵，适合刚起床的你。全程地板动作，不会打扰到任何人。',
            'duration_minutes': 5,
            'mood_tag': 'low_energy',
            'space_tag': 'room',
            'silent_mode': True,
            'icon': '🌅',
            'xp_reward': 20,
            'order': 1,
            'exercises': [
                ('颈部舒缓', '慢慢转动颈部，左三圈右三圈，感受颈椎的放松', 30, '轻轻地，不用着急，按照你自己的节奏来'),
                ('肩部绕环', '双肩向前画圈，再向后画圈，每个方向5次', 30, '放松肩膀，把压力都放下来'),
                ('坐姿体侧屈', '坐在椅子上或床上，身体向一侧缓缓倾斜，感受侧腰的拉伸', 40, '弯到你舒服的程度就好，不用勉强'),
                ('手腕脚踝活动', '转动手腕和脚踝，让关节润滑起来', 30, '小幅度转动就可以'),
                ('深呼吸收束', '闭眼，鼻子缓缓吸气4秒，嘴巴慢慢呼气6秒', 60, '感受空气进入身体，再缓缓离开'),
                ('猫式伸展', '跪姿，吸气拱背低头，呼气塌腰抬头，轻柔进行', 50, '动作幅度不用太大，舒服就好'),
                ('婴儿式放松', '跪坐，身体前倾趴下，额头贴地，完全放松', 60, '就这样待一会，你做得很好'),
            ],
        },
        {
            'name': '书桌旁微运动',
            'description': '在你最常待的书桌旁就能完成的训练。不用换衣服，不用铺瑜伽垫，站起来就能开始。',
            'duration_minutes': 5,
            'mood_tag': 'normal',
            'space_tag': 'dorm',
            'silent_mode': True,
            'icon': '🪑',
            'xp_reward': 25,
            'order': 2,
            'exercises': [
                ('坐姿抬腿', '坐在椅子上，交替抬腿，每条腿10次', 40, '不用太高，轻轻抬起放下就好'),
                ('椅子深蹲', '站在椅子前面，缓缓坐下再站起，不用完全坐下去', 30, '如果觉得累可以手扶桌边'),
                ('站姿侧抬腿', '手扶椅背，一条腿向侧面缓缓抬起再放下', 40, '幅度不用大，稳住身体'),
                ('手臂后伸', '双手在背后交握，缓缓向上抬，感受胸前的拉伸', 30, '抬到你舒服的高度就行'),
                ('坐姿转体', '坐在椅子上，身体缓缓向左转，停留片刻，再向右转', 40, '转动的时候保持呼吸顺畅'),
                ('脚踝写字', '坐在椅子上，抬起一只脚，用脚尖在空中写自己的名字', 30, '这是训练专注力的好方法'),
                ('闭眼静坐', '坐直身体，闭眼，专注于呼吸30秒', 30, '你刚刚完成了一组训练，做得不错'),
            ],
        },
        {
            'name': '基础全身激活',
            'description': '10分钟的全身训练，覆盖主要肌群。全程静音动作，不跳跃不跑动，宿舍房间都能做。',
            'duration_minutes': 10,
            'mood_tag': 'normal',
            'space_tag': 'any',
            'silent_mode': True,
            'icon': '💪',
            'xp_reward': 40,
            'order': 3,
            'exercises': [
                ('原地踏步', '原地轻轻踏步，手臂自然摆动，热身全身', 60, '先让身体热起来，不用急'),
                ('靠墙静蹲', '背靠墙壁，缓缓下蹲到大腿与地面平行，保持', 45, '坚持住，你可以的'),
                ('平板支撑', '手肘撑地，身体保持一条直线', 30, '收紧腹部，保持呼吸'),
                ('仰卧臀桥', '躺下屈膝，臀部缓缓抬起再放下', 45, '感受臀部的发力'),
                ('跪姿俯卧撑', '膝盖着地做俯卧撑，降低难度但效果不减', 40, '身体保持直线，下到自己能控制的高度'),
                ('鸟狗式', '跪姿，交替抬起对侧手臂和腿', 50, '保持身体稳定，不要晃动'),
                ('侧卧抬腿', '侧躺，上方腿缓缓抬起再放下', 45, '感受大腿外侧的发力'),
                ('死虫式', '仰卧，交替伸展对侧手脚', 50, '核心收紧，腰部贴地'),
                ('仰卧抱膝', '仰卧，双手抱膝向胸口靠拢', 40, '感受下背部的放松'),
                ('摊尸式放松', '完全平躺，四肢自然伸展，闭眼放松', 60, '你完成了一次完整的训练，很棒'),
            ],
        },
        {
            'name': '焦虑舒缓练习',
            'description': '当你感到焦虑不安时，这组训练能帮你重新连接身体，找回平静。以呼吸和温和拉伸为主。',
            'duration_minutes': 10,
            'mood_tag': 'anxious',
            'space_tag': 'any',
            'silent_mode': True,
            'icon': '🧘',
            'xp_reward': 35,
            'order': 4,
            'exercises': [
                ('4-7-8呼吸法', '坐直，鼻子吸气4秒，屏息7秒，嘴巴呼气8秒', 60, '如果7秒太长，按你自己的节奏来'),
                ('颈部放松', '头部缓缓前倾、后仰、左右侧倾，每个方向停留10秒', 60, '不要用力拉伸，自然下落就好'),
                ('肩部放松', '双肩用力耸起靠近耳朵，保持3秒后完全放松', 45, '感受紧张和放松的对比'),
                ('坐姿前屈', '坐在椅子上，身体缓缓前倾，双手自然下垂', 60, '把头完全交给重力，不用控制'),
                ('蝴蝶式', '脚掌相对，膝盖向两侧打开，身体缓缓前倾', 60, '膝盖不用压得太低，舒适最重要'),
                ('仰卧扭转', '躺下，双膝倒向一侧，头转向另一侧，停留后换边', 60, '感受脊柱的扭转和释放'),
                ('身体扫描', '闭眼，从脚趾到头顶，依次感受每个部位并放松', 90, '当你注意到某个部位紧张时，只是观察它，不评判'),
                ('感恩冥想', '闭眼，想一件今天值得感谢的小事', 60, '可以是任何事，一杯热水，一个微笑'),
                ('渐进放松', '从脚开始，依次收紧和放松每个肌群', 90, '感受放松后肌肉的沉重和温暖'),
                ('安静收束', '双手放在心口，感受心跳，做三次深呼吸', 45, '你已经平静下来了'),
            ],
        },
        {
            'name': '深夜助眠放松',
            'description': '适合睡前做的极限舒缓训练。灯光调暗，动作极慢，帮助你过渡到睡眠状态。',
            'duration_minutes': 5,
            'mood_tag': 'night',
            'space_tag': 'room',
            'silent_mode': True,
            'icon': '🌙',
            'xp_reward': 20,
            'order': 5,
            'exercises': [
                ('床上脚趾伸展', '躺在被子里，脚趾用力蜷缩后完全展开', 30, '重复几次，感受足部的疲劳释放'),
                ('腿部微动', '轻轻弯曲膝盖再伸直，动作幅度很小', 40, '像在水中一样缓慢移动'),
                ('骨盆倾斜', '仰卧屈膝，骨盆轻轻前倾后倾', 40, '感受腰部与床面的接触变化'),
                ('手臂伸展', '双手举过头顶，伸一个大大的懒腰', 30, '拉长身体，释放一天的紧张'),
                ('侧卧放松', '转向自己舒服的一侧，蜷缩成最舒服的姿势', 60, '像回到最安全的地方一样'),
                ('腹式呼吸', '一只手放腹部，感受吸气时腹部鼓起，呼气时腹部下沉', 60, '让呼吸变得缓慢而深沉'),
                ('晚安冥想', '闭眼，回顾今天的美好瞬间，对自己说晚安', 40, '今天的一切都已经过去了，好好休息'),
            ],
        },
        {
            'name': '今天不想动',
            'description': '没关系，这组超轻训练只需要2分钟。即使完全不想动，你也可以完成它。做完就算你赢。',
            'duration_minutes': 2,
            'mood_tag': 'low_energy',
            'space_tag': 'any',
            'silent_mode': True,
            'icon': '😌',
            'xp_reward': 10,
            'order': 0,
            'exercises': [
                ('坐姿深呼吸', '坐在你现在的位置上，闭眼，做三次深呼吸', 30, '只是呼吸，不需要做任何其他事情'),
                ('耸肩放松', '双肩耸起再放松，重复3次', 20, '这已经是运动了'),
                ('握拳展开', '双手用力握拳，再完全展开手指', 20, '感受手指的张力'),
                ('抬头低头', '缓缓抬头看天花板，再低头看胸口', 20, '温柔地活动颈部'),
                ('闭眼深呼吸', '闭眼，做一次尽可能长的深呼吸', 30, '你今天已经动过了，做得很好'),
            ],
        },
    ]

    created_count = 0
    for plan_data in plans_data:
        exercises_data = plan_data.pop('exercises')
        plan, created = TrainingPlan.objects.get_or_create(
            name=plan_data['name'],
            defaults=plan_data,
        )
        if created:
            created_count += 1
            for i, (name, desc, duration, voice) in enumerate(exercises_data):
                TrainingExercise.objects.create(
                    plan=plan,
                    name=name,
                    description=desc,
                    duration_seconds=duration,
                    voice_guide=voice,
                    order=i,
                )
        elif plan.exercises.count() == 0:
            for i, (name, desc, duration, voice) in enumerate(exercises_data):
                TrainingExercise.objects.create(
                    plan=plan,
                    name=name,
                    description=desc,
                    duration_seconds=duration,
                    voice_guide=voice,
                    order=i,
                )

    return created_count


def seed_achievements():
    achievements_data = [
        ('初次启程', '完成第一次训练', '🌟', 'first_session', 1, 30, False),
        ('三天打鱼', '累计训练3次', '🐟', 'total_sessions', 3, 40, False),
        ('坚持一周', '累计训练7次', '🔥', 'total_sessions', 7, 60, False),
        ('半月坚持', '累计训练15次', '💎', 'total_sessions', 15, 80, False),
        ('月度勇士', '累计训练30次', '👑', 'total_sessions', 30, 150, False),
        ('连续三天', '连续3天训练', '📅', 'streak_days', 3, 50, False),
        ('不间断周', '连续7天训练', '⚡', 'streak_days', 7, 100, False),
        ('起床困难户', '连续3天起床后训练', '🌄', 'streak_days', 3, 40, True),
        ('深夜陪伴者', '完成5次深夜训练', '🦉', 'night_owl', 5, 50, False),
        ('安静的灵魂', '完成10次舒缓训练', '🌸', 'gentle_soul', 10, 60, False),
        ('XP收集者', '累计获得500经验值', '⭐', 'total_xp', 500, 80, False),
        ('今天不想动', '完成"今天不想动"训练', '😌', 'total_sessions', 1, 20, True),
    ]

    created_count = 0
    for name, desc, icon, cond_type, cond_val, xp_reward, hidden in achievements_data:
        _, created = Achievement.objects.get_or_create(
            name=name,
            defaults={
                'description': desc,
                'icon': icon,
                'condition_type': cond_type,
                'condition_value': cond_val,
                'xp_reward': xp_reward,
                'is_hidden': hidden,
            },
        )
        if created:
            created_count += 1

    return created_count
