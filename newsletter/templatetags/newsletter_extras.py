from django import template
from newsletter.models import Newsletter

register = template.Library()

@register.filter
def active_newsletters_count(user):
    """Фильтр для подсчета активных рассылок пользователя."""
    return Newsletter.objects.filter(user=user, status='active').count()