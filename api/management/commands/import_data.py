import requests

from django.core.management.base import BaseCommand
from api.models import Community, Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        # https://projectrio-api-1.api.projectrio.app/games/?limit_games=15
        session = requests.Session()
        response = session.get(url='https://projectrio-api-1.api.projectrio.app/games/?limit_games=15&page=2')
        if response.ok:
            print(response.json())

