import os
from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv
from lib import utils


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_dotenv()

