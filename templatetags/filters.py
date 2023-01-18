from django import template
register = template.Library()

@register.filter
def calcPrice(value, discount):
    value = int(value)
    discount = int(discount)
    return (value*(100-discount)/100)

@register.filter
def calcAllPrice(value, discount, quantity):
    value = int(value)
    discount = int(discount)
    return ((value*(100-discount)/100)*quantity)

@register.filter
def format_money(value, num_decimals=3, seperator='.'):
    value = str(int(value))
    if len(value) <= num_decimals:
        return value
    parts = []
    while value:
        parts.append(value[-num_decimals:])
        value = value[:-num_decimals]
    parts.reverse()
    return seperator.join(parts)

@register.filter
def toStr(integer):
    return str(integer)