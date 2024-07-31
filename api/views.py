import json
from api.authentication import TokenAuthentication
from api.helpers import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class GenericView(APIView):
    """
    This will get or create specified object
    GET: Returns all or specific specified object
    POST: Creates specified object
    """
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        mapping = {
            'tag': 'Tag',
            'tagset': 'TagSet',
            'community': 'Community',
            'communityuser': 'CommunityUser'
        }
        return JsonResponse(generic_get_request_json(model_name=mapping.get(request.path.split('/')[3]),
                                                     request=request, **kwargs))

    def post(self, request, *args, **kwargs):
        mapping = {
            'tag': 'Tag',
            'tagset': 'TagSet',
            'community': 'Community',
            'communityuser': 'CommunityUser'
        }
        return JsonResponse(generic_post_request_json(model_name=mapping.get(request.path.split('/')[3]),
                                                      request=request, **kwargs))


class v1_tag_list(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # name = models.CharField(max_length=32, unique=True)
        # tag_type = models.CharField(max_length=16)
        # description = models.CharField(max_length=300)
        # active = models.BooleanField(default=True)
        # date_created
        output = {
            "Tags": [
                {
                    "active": True,
                    "comm_id": 1,
                    "date_created": 1677633618,
                    "desc": "Both teams always have 5 stars",
                    "gecko_code": "00892ad6 000100ff\n",
                    "gecko_code_desc": "Both teams always have 5 stars.",
                    "id": 7,
                    "name": "Unlimited Stars",
                    "type": "Gecko Code"
                },
                {
                    "active": True,
                    "comm_id": 1,
                    "date_created": 1679262056,
                    "desc": "Both players will use the random teams with random captains",
                    "id": 16,
                    "name": "Draft Randoms",
                    "type": "Component"
                },
                {
                    "active": True,
                    "comm_id": 1,
                    "date_created": 1679890869,
                    "desc": "Disables the built in manual fielder select code. Can be overriden by a gecko code version of MFS",
                    "id": 39,
                    "name": "Disable Manual Fielder Select",
                    "type": "Client Code"
                },
            ]
        }

        tags = list()
        result = models.Tag.objects.filter(tag_type__in=["Gecko Code", "Client Code", "Component"])
        for tag in result:
            tag_dict = tag.to_dict()
            if tag.tag_type == 'Gecko Code':
                result = models.GeckoCodeTag.objects.filter(tag__pk=tag.pk).first()
                if result is None:
                    tag_dict = tag_dict | result.to_dict()
            else:
                tag_dict = tag_dict | {"gecko_code_desc": "", "gecko_code": ""}
            tags.append(tag_dict)
        return JsonResponse({'Tags': tags})
