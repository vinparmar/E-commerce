from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except Exception:
        try:
            return int(value) * int(arg)
        except Exception:
            return 0
