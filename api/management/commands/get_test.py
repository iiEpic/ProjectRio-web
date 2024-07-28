import os
import random
import string
from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv
from lib import utils
from api import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        random_numbers = random.sample(range(1, 200 + 1), 30)

        for random_number in random_numbers:
            user = models.RioUser.objects.filter(pk=random_number).first()
            user.private = True
            user.save()
