import os

from django.core.management.base import BaseCommand
import json
from api.models import Community, Tag
import os
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.abspath(__file__).split('/')[:-1]
        path = os.path.join(os.sep, *path, 'tags.json')
        # I want this to pull the old Tags from ProjectRio
        with open(path, 'r') as f:
            data = json.load(f)
        # name = models.CharField(max_length=32, unique=True)
        # community = models.ForeignKey(Community, on_delete=models.CASCADE)
        # tag_type = models.CharField(max_length=16)
        # description = models.CharField(max_length=300)
        # active = models.BooleanField(default=True)
        # date_created = models.DateTimeField(auto_created=True, auto_now=True)
        # gecko_code = models.TextField()
        # gecko_code_desc = models.CharField(max_length=255)
        for tag in data:
            community = Community.objects.filter(id=tag['comm_id']).first()
            if community is not None:
                tag_data = {
                    'name': tag['name'],
                    'community': community,
                    'tag_type': tag['type'],
                    'description': tag['desc'],
                    'active': tag['active'],
                    'date_created': datetime.fromtimestamp(tag['date_created']),
                    'last_modified': datetime.fromtimestamp(tag['date_created']),
                }
                if 'gecko_code' in tag:
                    tag_data['gecko_code'] = tag['gecko_code']
                    tag_data['gecko_code_desc'] = tag['gecko_code_desc']

                tag_obj = Tag.objects.filter(name=tag['name']).first()
                if tag_obj is None:
                    tag_obj = Tag.objects.create(**tag_data)
