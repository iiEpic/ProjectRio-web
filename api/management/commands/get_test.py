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

        print(random_numbers)
        for x in range(0, 200):
            rand = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))
            models.RioUser.objects.create(
                username=rand,
                email=f'{rand}@email.com',
                password=rand,
            )
