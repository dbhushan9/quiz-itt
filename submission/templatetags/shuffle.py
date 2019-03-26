import random
from django import template
register = template.Library()

@register.filter
def shuffle(arg):
    print(arg)
    arg = list(arg)
    random.shuffle(arg)
    return arg