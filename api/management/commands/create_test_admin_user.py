import random
import string
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from api import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        if models.RioUser.objects.filter(user__username='admin').first() is None:
            api_key = models.ApiKey.objects.create(
                api_key=''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16)),
                pings_daily=1,
                pings_weekly=1,
                last_ping_date=1,
                total_pings=0,
            )
            rio_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))
            models.RioUser.objects.create(
                user=User.objects.filter(username='admin').first(),
                api_key=api_key,
                rio_key=rio_key
            )
