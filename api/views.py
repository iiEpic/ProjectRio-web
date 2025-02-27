import json
import random

from api.authentication import TokenAuthentication
from api.forms import PopulateDBForm
from api.helpers import *
from api.models import CommunityUser, Game, OngoingGame, TagSet, Token
from datetime import datetime, UTC
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
            'communityuser': 'CommunityUser',
            'characters': 'Character',
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


class PopulateDB(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return JsonResponse({'results': 'GET method not valid. Only POST.'})

    def post(self, request, *args, **kwargs):

        start_time = datetime.now(tz=UTC)

        form = PopulateDBForm(request.data)

        if not form.is_valid():
            return JsonResponse({'results': 'Invalid data sent', 'errors': form.errors})

        # Ignore game versions below 1.9.5
        version_split = form.cleaned_data['version'].split('.')
        if version_split[0] == '1' and version_split[1] <= '9' and int(version_split[2]) <= 4:
            return JsonResponse({'results': 'Not accepting games from clients below 1.9.5'})

        # Ignore game if it's a CPU game
        if form.cleaned_data['home_player'] == "CPU" or form.cleaned_data['away_player'] == "CPU":
            return JsonResponse({'results': 'Database does not accept CPU games'})

        # Ensure both players actually exist as Rio Users
        home_player = Token.objects.filter(key=form.cleaned_data['home_player']).first()
        away_player = Token.objects.filter(key=form.cleaned_data['away_player']).first()
        if home_player is None:
            return JsonResponse({'results': 'Home player not found.'})
        if away_player is None:
            return JsonResponse({'results': 'Away player not found.'})

        home_player = home_player.user.riouser
        away_player = away_player.user.riouser

        # Check if users are verified
        if not home_player.verified:
            return JsonResponse({'results': 'Home player not verified.'})
        if not away_player.verified:
            return JsonResponse({'results': 'Away player not verified.'})

        # Detect invalid games
        innings_selected = form.cleaned_data['innings_selected']
        innings_played = form.cleaned_data['innings_played']
        score_difference = abs(form.cleaned_data['home_score'] - form.cleaned_data['away_score'])
        is_valid = False if innings_played < innings_selected and score_difference < 10 else True

        if not is_valid:
            return JsonResponse({'results': 'Invalid Game: Innings Played < Innings Selected & Score Difference < 10'})

        # Validate the tagset ID
        tag_set = TagSet.objects.filter(id=form.cleaned_data['tagset_id']).first()
        if tag_set is None:
            return JsonResponse({'results': f'Could not find tagset with id, {form.cleaned_data["tagset_id"]}'})

        # Confirm that both users are community members for given TagSet
        # Get TagSet obj to verify users

        home_comm_user = CommunityUser.objects.filter(user=home_player, community=tag_set.community).first()
        away_comm_user = CommunityUser.objects.filter(user=away_player, community=tag_set.community).first()

        if home_comm_user is None or away_comm_user is None:
            return JsonResponse({'results': 'One or both users are not part of the community for this TagSet.'})

        # TODO Look into removing this step. GameID SHOULD be guaranteed by checking in ongoing_games now
        # Reroll game id until unique one is found
        unique_id = False
        game_id = int(form.cleaned_data['game_id'].replace(',', ''), 16)
        while not unique_id:
            game = Game.objects.filter(game_id=game_id).first()
            if game is None:
                unique_id = True
            else:
                game_id = random.getrandbits(32)

        # Delete ongoing game row once game is submitted
        OngoingGame.objects.filter(game_id=game_id).delete()

        game = Game.objects.create(
            game_id=game_id,
            away_player=away_player,
            home_player=home_player,
            date_time_start=int(form.cleaned_data['date_start']),
            date_time_end=int(form.cleaned_data['date_end']),
            netplay=form.cleaned_data['netplay'],
            stadium_id=form.cleaned_data['stadium_id'],
            away_score=form.cleaned_data['away_score'],
            home_score=form.cleaned_data['home_score'],
            innings_selected=form.cleaned_data['innings_selected'],
            innings_played=form.cleaned_data['innings_played'],
            valid=is_valid,
            average_ping=form.cleaned_data['average_ping'],
            lag_spikes=form.cleaned_data['lag_spikes'],
            version=form.cleaned_data['version'],
        )
        if not form.cleaned_data['quitter']:
            game.quitter = form.cleaned_data['quitter']
            game.save()

        end_time = datetime.now(tz=UTC)
        elapsed_time = (end_time - start_time).total_seconds()

        return JsonResponse(
            {
                'results': 'Game successfully uploaded!',
                'start_time': start_time,
                'end_time': end_time,
                'elapsed_time': f'{elapsed_time * 60} seconds',
                'game_id': game.id
            }
        )

#
#     # Ignore game if it's a CPU game
#     if request.json['Home Player'] == "CPU" or request.json['Away Player'] == "CPU":
#         return abort(400, 'Database does not accept CPU games')
