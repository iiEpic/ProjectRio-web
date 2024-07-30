from django import template
from api import models

register = template.Library()


@register.simple_tag
def get_user_api_key(username):
    user_object = models.RioUser.objects.filter(user__username__iexact=username).first()
    if user_object is None:
        return None
    return user_object.api_key if user_object.api_key is not None else None


@register.simple_tag
def get_user_rio_key(username):
    user_object = models.RioUser.objects.filter(user__username__iexact=username).first()
    if user_object is None:
        return None
    return user_object.rio_key.key if user_object.rio_key is not None else None
