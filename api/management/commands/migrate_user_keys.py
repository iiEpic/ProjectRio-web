import secrets
from api import models
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):

        for user in models.RioUser.objects.all():
            print(f'Migrating Rio and API keys for user,  {user.username()}')

            if user.api_key is None:
                print('test')
                # Create a token for API Key
                token = models.Token.objects.create(
                    key=secrets.token_urlsafe(32),
                    user=user.user,
                    name='api_key'
                )
                api_key = models.ApiKey.objects.create(
                    token=token
                )
                user.api_key = api_key
                user.save()
            else:
                # Convert to new format
                pass

            if user.rio_key is None:
                # Create a token for Rio Key
                token = models.Token.objects.create(
                    key=secrets.token_urlsafe(32),
                    user=user.user,
                    name='rio_key'
                )
                user.rio_key = token
                user.save()
            else:
                # Convert to new format
                pass

            print(f'Completed {user.username()} Rio and API keys.')
