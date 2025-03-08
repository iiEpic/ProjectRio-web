from django import template
from api import models

register = template.Library()


@register.simple_tag
def get_user_token(username):
    token_object = models.Token.objects.filter(user__username__iexact=username).first()
    if token_object is None:
        return None
    return token_object.key if token_object.key is not None else None

