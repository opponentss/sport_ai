from django.core.management.base import BaseCommand
from checkin.models import ExerciseType
from game_system.models import Achievement, DailyMission


EXERCISE_TYPES = [
    ('俯卧撑', 'home', 'beginner', 7.0, '🤸', 2, 1, 0),
    ('深蹲', 'home', 'beginner', 6.0, '🦵', 3, 1, 0),
    ('平板支撑', 'home', 'intermediate', 5.0, '🪨', 1, 2, 0),
    ('开合跳', 'home', 'beginner', 10.0, '⭐', 1, 2, 1),
    ('跳绳', 'home', 'intermediate', 12.0, '🪢', 1, 3, 2),
    ('瑜伽', 'home', 'intermediate', 4.0, '🧘', 0, 1, 2),
    ('健身环', 'home', 'beginner', 6.0, '🎮', 1, 1, 1),
    ('波比跳', 'home', 'challenge', 14.0, '🔥', 2, 3, 2),
    ('跑步', 'outdoor', 'beginner', 10.0, '🏃', 1, 3, 0),
    ('骑行', 'outdoor', 'intermediate', 8.0, '🚴', 1, 2, 0),
    ('散步', 'outdoor', 'beginner', 3.0, '🚶', 0, 1, 0),
    ('登山', 'outdoor', 'challenge', 9.0, '⛰️', 2, 3, 1),
    ('哑铃训练', 'gym', 'beginner', 6.0, '🏋️', 3, 1, 0),
    ('杠铃训练', 'gym', 'intermediate', 8.0, '🏋️‍♂️', 3, 1, 0),
    ('弹力带训练', 'gym', 'beginner', 4.0, '🩹', 2, 1, 0),
    ('引体向上', 'gym', 'challenge', 10.0, '💪', 3, 2, 1),
    ('椭圆机', 'cardio', 'beginner', 8.0, '🔄', 0, 3, 0),
    ('动感单车', 'cardio', 'intermediate', 11.0, '🚲', 1, 3, 0),
    ('划船机', 'cardio', 'intermediate', 9.0, '🚣', 2, 3, 0),
    ('拉伸', 'stretch', 'beginner', 2.0, '🧘‍♀️', 0, 0, 2),
]

ACHIEVEMENTS = [
    ('初次挥汗', '完成第一次运动打卡', '💧', 'checkin', 'total_checkins', 1, 20, 1),
    ('十次修行', '累计完成10次运动打卡', '🔟', 'checkin', 'total_checkins', 10, 50, 2),
    ('百炼成钢', '累计完成100次运动打卡', '💯', 'checkin', 'total_checkins', 100, 200, 3),
    ('运动新手', '累计运动60分钟', '⏱️', 'checkin', 'total_exercise_minutes', 60, 50, 4),
    ('运动达人', '累计运动600分钟', '🏅', 'checkin', 'total_exercise_minutes', 600, 100, 5),
    ('运动狂人', '累计运动3000分钟', '🔱', 'checkin', 'total_exercise_minutes', 3000, 300, 6),
    ('饮食管理者', '累计记录10次三餐', '🍽️', 'meal', 'total_meals', 10, 50, 7),
    ('营养大师', '累计记录50次三餐', '🥗', 'meal', 'total_meals', 50, 100, 8),
    ('睡眠新手', '累计记录5次睡眠', '😴', 'sleep', 'total_sleeps', 5, 30, 9),
    ('睡眠专家', '累计记录30次睡眠', '🌟', 'sleep', 'total_sleeps', 30, 80, 10),
    ('初级觉醒', '达到等级5', '⬆️', 'special', 'level_reach', 5, 100, 11),
    ('中极突破', '达到等级15', '⚡', 'special', 'level_reach', 15, 200, 12),
    ('高级进化', '达到等级30', '🔮', 'special', 'level_reach', 30, 500, 13),
    ('周日也在运动', '周日完成运动打卡', '📅', 'special', 'strength_reach', 3, 30, 14),
    ('凌晨的运动魂', '凌晨0-6点完成运动打卡', '🌙', 'special', 'strength_reach', 5, 50, 15),
]

DAILY_MISSIONS = [
    ('今日运动', '今天完成至少1次运动打卡', 'checkin', 1, 20, 1),
    ('燃烧卡路里', '今天运动时长至少30分钟', 'duration', 30, 30, 2),
    ('饮食管理', '今天记录至少2餐', 'meal', 2, 20, 3),
    ('早睡早起', '今天记录睡眠情况', 'sleep', 1, 15, 4),
]


class Command(BaseCommand):
    help = '初始化游戏化系统的初始数据（运动类型、成就、每日任务）'

    def handle(self, *args, **options):
        self.stdout.write('正在初始化运动类型...')
        for name, category, difficulty, cpm, icon, sg, eg, ag in EXERCISE_TYPES:
            obj, created = ExerciseType.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'difficulty': difficulty,
                    'calories_per_minute': cpm,
                    'icon': icon,
                    'strength_gain': sg,
                    'endurance_gain': eg,
                    'agility_gain': ag,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  创建运动类型: {icon} {name}'))
            else:
                self.stdout.write(f'  已存在: {icon} {name}')

        self.stdout.write('正在初始化成就...')
        for name, desc, icon, cat, ct, cv, xp, order in ACHIEVEMENTS:
            obj, created = Achievement.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'icon': icon,
                    'category': cat,
                    'condition_type': ct,
                    'condition_value': cv,
                    'xp_reward': xp,
                    'order': order,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  创建成就: {icon} {name}'))
            else:
                self.stdout.write(f'  已存在: {icon} {name}')

        self.stdout.write('正在初始化每日任务...')
        for title, desc, mt, tv, xp, order in DAILY_MISSIONS:
            obj, created = DailyMission.objects.get_or_create(
                title=title,
                defaults={
                    'description': desc,
                    'mission_type': mt,
                    'target_value': tv,
                    'xp_reward': xp,
                    'order': order,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  创建任务: {title}'))
            else:
                self.stdout.write(f'  已存在: {title}')

        self.stdout.write(self.style.SUCCESS('\n✅ 游戏化系统数据初始化完成！'))
