import requests

from django.core.management.base import BaseCommand
from api.models import Permission, Role


class Command(BaseCommand):
    def handle(self, *args, **options):
        permission_names = ['Tag', 'TagSet', 'CommunityUser']
        actions = ['Create', 'Edit', 'Delete']
        permissions = []
        for name in permission_names:
            for action in actions:
                permission = Permission.objects.get_or_create(
                    name=f'{action} {name}',
                    description=f'Default permissions to {action.lower()} a {name}'
                )
                permissions.append(permission[0])

        role_names = ['Admin', 'Moderator', 'Member']
        for name in role_names:
            role = Role.objects.get_or_create(
                name=name,
                description=f'Default role for {name}'
            )
            role = role[0]
            if name == 'Admin':
                [role.permissions.add(i) for i in permissions]
            if name == 'Moderator':
                for permission in permissions:
                    if 'CommunityUser' in permission.name:
                        role.permissions.add(permission)

