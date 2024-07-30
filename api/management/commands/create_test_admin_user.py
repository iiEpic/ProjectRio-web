import secrets
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from api import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        if models.RioUser.objects.filter(user__username='admin').first() is None:
            api_token = models.Token.objects.create(
                key=secrets.token_urlsafe(32),
                user=User.objects.filter(username='admin').first(),
                name='api_key'
            )
            api_key = models.ApiKey.objects.create(
                token=api_token
            )
            rio_token = models.Token.objects.create(
                key=secrets.token_urlsafe(32),
                user=User.objects.filter(username='admin').first(),
                name='rio_key'
            )
            models.RioUser.objects.create(
                user=User.objects.filter(username='admin').first(),
                api_key=api_key,
                rio_key=rio_token
            )
