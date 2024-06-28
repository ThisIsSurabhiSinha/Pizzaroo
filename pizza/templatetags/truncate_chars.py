from django import template

register = template.Library()

@register.filter
def truncate_chars(value, arg):
    try:
        arg = int(arg)  
    except ValueError:
        return value  

    if len(value) > arg:
        return value[:arg] + '...'
    elif len(value) < arg:
        return value + " " * (arg - len(value))
    
    else:
        return value
