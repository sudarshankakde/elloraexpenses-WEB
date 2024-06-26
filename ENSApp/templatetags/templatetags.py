from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='in_group')
def in_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Group.DoesNotExist:
        return False
      

  
@register.simple_tag
def sum_field(expenses_with_changes, field_name):
    return sum(getattr(expense['expense'], field_name, 0) for expense in expenses_with_changes)
