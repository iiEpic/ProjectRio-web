import json
import random

from api.authentication import TokenAuthentication
from api.forms import PopulateDBForm, TagForm
from api import models as api_models
from datetime import datetime, UTC
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView


# Create your views here.
class Tag(APIView):
    authentication_classes = [JWTAuthentication, TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tag_objects = api_models.Tag.objects.filter(tag_type__in=['Gecko Code', 'Client Code', 'Component'])

        if request.query_params:
            query = Q()
            for k, v in request.query_params.items():
                query &= Q(**{k: v})  # Build the AND query
            tag_objects = tag_objects.filter(query)

        return JsonResponse({'status': 'successful', 'tags': [i.to_dict() for i in tag_objects], 'count': len(tag_objects)})

    def post(self, request, *args, **kwargs):
        form = TagForm(request.POST)
        rio_user = api_models.RioUser.objects.filter(user=self.request.user).first()

        if form.is_valid():
            # Check if user has permissions to create a Tag
            # Check if user has permissions to create a Tag for this specific community

            # Make sure that tag does not use the same name as an existing tag, comm, or tag_set
            tag = api_models.Tag.objects.filter(name__iexact=form.cleaned_data.get('name')).first()
            comm_name_check = api_models.Community.objects.filter(name__iexact=form.cleaned_data.get('name')).first()
            tag_set = api_models.TagSet.objects.filter(name__iexact=form.cleaned_data.get('name')).first()
            if tag or comm_name_check or tag_set:
                form.add_error('name', 'Conflicting tag, community or tagset name.')
                return JsonResponse({'status': 'failed', 'errors': form.errors})

            community = api_models.Community.objects.filter(name__iexact=form.cleaned_data.get('community_name')).first()
            if community is None:
                form.add_error('community_name', 'Community does not exist by that name.')
            else:
                # Check if the user has access to view this community
                community_user = api_models.CommunityUser.objects.filter(community=community, user=rio_user).first()
                if community_user is None or community_user.banned:
                    form.add_error('community_name', 'Community does not exist by that name.')
                else:
                    if not community_user.admin:
                        # Now check if the user has admin status to add a Tag
                        form.add_error('community_name',
                                       'You do not have permissions to create a tag for this community. '
                                       'Please ask an admin.')
            # All our checks are done, check if we have any errors
            if form.errors:
                return JsonResponse({'status': 'failed', 'errors': form.errors})
            else:
                # No errors, create our Tag
                form.cleaned_data['community'] = community
                form.cleaned_data.pop('community_name')
                tag = api_models.Tag.objects.create(**form.cleaned_data)
                return JsonResponse({'status': 'successful', 'tags': [tag.to_dict()]})
        # Form had errors originally
        return JsonResponse({'status': 'failed', 'errors': form.errors})


class TagSet(APIView):
    authentication_classes = [JWTAuthentication, TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tagset_objects = api_models.TagSet.objects.all()

        if request.query_params:
            query = Q()
            for k, v in request.query_params.items():
                query &= Q(**{k: v})  # Build the AND query
            tagset_objects = tagset_objects.filter(query)

        return JsonResponse(
            {'status': 'successful', 'tagsets': [i.to_dict() for i in tagset_objects], 'count': len(tagset_objects)})


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
        home_player = api_models.Token.objects.filter(key=form.cleaned_data['home_player']).first()
        away_player = api_models.Token.objects.filter(key=form.cleaned_data['away_player']).first()
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

        home_comm_user = api_models.CommunityUser.objects.filter(user=home_player, community=tag_set.community).first()
        away_comm_user = api_models.CommunityUser.objects.filter(user=away_player, community=tag_set.community).first()

        if home_comm_user is None or away_comm_user is None:
            return JsonResponse({'results': 'One or both users are not part of the community for this TagSet.'})

        # TODO Look into removing this step. GameID SHOULD be guaranteed by checking in ongoing_games now
        # Reroll game id until unique one is found
        unique_id = False
        game_id = int(form.cleaned_data['game_id'].replace(',', ''), 16)
        while not unique_id:
            game = api_models.Game.objects.filter(game_id=game_id).first()
            if game is None:
                unique_id = True
            else:
                game_id = random.getrandbits(32)

        # Delete ongoing game row once game is submitted
        api_models.OngoingGame.objects.filter(game_id=game_id).delete()

        game = api_models.Game.objects.create(
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
