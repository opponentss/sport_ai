"""
自定义模板过滤器

提供在Django模板中使用的自定义过滤器。
"""

from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    获取字典中指定键的值

    用法：{{ my_dict|get_item:key }}

    Args:
        dictionary: Django模板中的字典对象
        key: 要获取的键

    Returns:
        字典中对应键的值，如果键不存在则返回空字符串
    """
    if dictionary is None:
        return ''
    return dictionary.get(key, '')
