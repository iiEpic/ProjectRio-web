import random
from .authentication import TokenAuthentication
from datetime import datetime, UTC
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .forms import PopulateDBForm
from .models import (
    Token, UserGroup, UserProfile, Character, CharacterChemistry,
    Community, Role, CommunityUser, Tag, TagSet, Game, GameRoster,
    GameEventSummary, GameEvent, Ladder
)
from .serializers import (
    UserGroupSerializer, UserProfileSerializer, CharacterSerializer,
    CharacterChemistrySerializer, CommunitySerializer, RoleSerializer,
    CommunityUserSerializer, TagSerializer, TagSetSerializer, GameSerializer,
    GameRosterSerializer, GameEventSummarySerializer, GameEventSerializer, LadderSerializer
)


class UserGroupDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserGroupSerializer(user_group)
        return Response(serializer.data)


class UserProfileDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            if user_profile.private and not self.request.user.is_staff:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)


class CharacterDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, identifier):  # Identifier can be pk, slug, or name
        try:
            # Try to retrieve by primary key (ID)
            character = Character.objects.get(pk=identifier)
        except ValueError:
            # Identifier is not an integer (primary key)
            try:
                # Try to retrieve by slug
                character = Character.objects.get(slug__iexact=identifier)
            except Character.DoesNotExist:
                # Try to retrieve by name
                try:
                    character = Character.objects.get(name__iexact=identifier)
                except Character.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        except Character.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CharacterSerializer(character)
        return Response(serializer.data)


class CharacterChemistryDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            character_chemistry = CharacterChemistry.objects.get(pk=pk)
        except CharacterChemistry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CharacterChemistrySerializer(character_chemistry)
        return Response(serializer.data)


class CommunityDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            community = Community.objects.get(pk=pk)
            if community.private and not self.request.user.is_staff:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Community.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommunitySerializer(community)
        return Response(serializer.data)


class RoleDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role)
        return Response(serializer.data)


class CommunityUserDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            community_user = CommunityUser.objects.get(pk=pk)
        except CommunityUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommunityUserSerializer(community_user)
        return Response(serializer.data)


class TagDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TagSerializer(tag)
        return Response(serializer.data)


class TagSetDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            tag_set = TagSet.objects.get(pk=pk)
        except TagSet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TagSetSerializer(tag_set)
        return Response(serializer.data)


class GameDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GameSerializer(game)
        return Response(serializer.data)


class GameRosterDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            game_roster = GameRoster.objects.get(pk=pk)
        except GameRoster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GameRosterSerializer(game_roster)
        return Response(serializer.data)


class GameEventSummaryDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            game_event_summary = GameEventSummary.objects.get(pk=pk)
        except GameEventSummary.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GameEventSummarySerializer(game_event_summary)
        return Response(serializer.data)


class GameEventDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            game_event = GameEvent.objects.get(pk=pk)
        except GameEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GameEventSerializer(game_event)
        return Response(serializer.data)


class LadderDetail(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            ladder = Ladder.objects.get(pk=pk)
        except Ladder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LadderSerializer(ladder)
        return Response(serializer.data)


class UserGroupList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_groups = UserGroup.objects.all()
        serializer = UserGroupSerializer(user_groups, many=True)
        return Response(serializer.data)


class UserProfileList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if self.request.user.is_staff:
            user_profiles = UserProfile.objects.all()
        else:
            user_profiles = UserProfile.objects.filter(private=False)
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data)


class CharacterList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        characters = Character.objects.all()
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)


class CharacterChemistryList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        character_chemistries = CharacterChemistry.objects.all()
        serializer = CharacterChemistrySerializer(character_chemistries, many=True)
        return Response(serializer.data)


class CommunityList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_superuser:
            communities = Community.objects.all()
        else:
            public_communities = Community.objects.filter(private=False)
            member_communities = Community.objects.filter(communityuser__user=user, communityuser__status='active')
            communities = (public_communities | member_communities).distinct()
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data)


class RoleList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)


class CommunityUserList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        community_users = CommunityUser.objects.all()
        serializer = CommunityUserSerializer(community_users, many=True)
        return Response(serializer.data)


class TagList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class TagSetList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tag_sets = TagSet.objects.all()
        serializer = TagSetSerializer(tag_sets, many=True)
        return Response(serializer.data)


class GameList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)


class GameRosterList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        game_rosters = GameRoster.objects.all()
        serializer = GameRosterSerializer(game_rosters, many=True)
        return Response(serializer.data)


class GameEventSummaryList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        game_event_summaries = GameEventSummary.objects.all()
        serializer = GameEventSummarySerializer(game_event_summaries, many=True)
        return Response(serializer.data)


class GameEventList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        game_events = GameEvent.objects.all()
        serializer = GameEventSerializer(game_events, many=True)
        return Response(serializer.data)


class LadderList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ladders = Ladder.objects.all()
        serializer = LadderSerializer(ladders, many=True)
        return Response(serializer.data)


class PopulateDB(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'results': 'GET method not valid. Only POST.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        start_time = datetime.now(tz=UTC)
        form = PopulateDBForm(request.data)

        if not form.is_valid():
            return Response({'results': 'Invalid data sent', 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        version_split = form.cleaned_data['version'].split('.')
        if version_split[0] == '1' and version_split[1] <= '9' and int(version_split[2]) <= 4:
            return Response({'results': 'Not accepting games from clients below 1.9.5'}, status=status.HTTP_400_BAD_REQUEST)

        if form.cleaned_data['home_player'] == "CPU" or form.cleaned_data['away_player'] == "CPU":
            return Response({'results': 'Database does not accept CPU games'}, status=status.HTTP_400_BAD_REQUEST)

        home_player_token = Token.objects.filter(key=form.cleaned_data['home_player']).first()
        away_player_token = Token.objects.filter(key=form.cleaned_data['away_player']).first()

        if not home_player_token:
            return Response({'results': 'Home player not found.'}, status=status.HTTP_400_BAD_REQUEST)
        if not away_player_token:
            return Response({'results': 'Away player not found.'}, status=status.HTTP_400_BAD_REQUEST)

        home_player = home_player_token.user.riouser
        away_player = away_player_token.user.riouser

        if not home_player.verified:
            return Response({'results': 'Home player not verified.'}, status=status.HTTP_400_BAD_REQUEST)
        if not away_player.verified:
            return Response({'results': 'Away player not verified.'}, status=status.HTTP_400_BAD_REQUEST)

        innings_selected = form.cleaned_data['innings_selected']
        innings_played = form.cleaned_data['innings_played']
        score_difference = abs(form.cleaned_data['home_score'] - form.cleaned_data['away_score'])
        is_valid = innings_played >= innings_selected or score_difference >= 10

        if not is_valid:
            return Response({'results': 'Invalid Game: Innings Played < Innings Selected & Score Difference < 10'}, status=status.HTTP_400_BAD_REQUEST)

        tag_set = TagSet.objects.filter(id=form.cleaned_data['tagset_id']).first()
        if not tag_set:
            return Response({'results': f'Could not find tagset with id, {form.cleaned_data["tagset_id"]}'}, status=status.HTTP_400_BAD_REQUEST)

        home_comm_user = CommunityUser.objects.filter(user=home_player, community=tag_set.community).first()
        away_comm_user = CommunityUser.objects.filter(user=away_player, community=tag_set.community).first()

        if not home_comm_user or not away_comm_user:
            return Response({'results': 'One or both users are not part of the community for this TagSet.'}, status=status.HTTP_400_BAD_REQUEST)

        game_id = int(form.cleaned_data['game_id'].replace(',', ''), 16)
        while Game.objects.filter(game_id=game_id).exists():
            game_id = random.getrandbits(32)

        Game.objects.filter(game_id=game_id).delete()

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
            quitter=form.cleaned_data['quitter'] if form.cleaned_data['quitter'] else None,
        )

        end_time = datetime.now(tz=UTC)
        elapsed_time = (end_time - start_time).total_seconds()

        return Response(
            {
                'results': 'Game successfully uploaded!',
                'start_time': start_time,
                'end_time': end_time,
                'elapsed_time': f'{elapsed_time} seconds',
                'game_id': game.id,
            },
            status=status.HTTP_201_CREATED,
        )


#
# # Create your views here.
# class Tag(APIView):
#     authentication_classes = [JWTAuthentication, TokenAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     INVALID_NAMES = [
#         'create'
#     ]
#
#     def get(self, request, *args, **kwargs):
#         tag_objects = api_models.Tag.objects.filter(tag_type__in=['Gecko Code', 'Client Code', 'Component'])
#
#         if request.query_params:
#             query = Q()
#             for k, v in request.query_params.items():
#                 query &= Q(**{k: v})  # Build the AND query
#             tag_objects = tag_objects.filter(query)
#
#         return JsonResponse({'status': 'successful', 'tags': [i.to_dict() for i in tag_objects], 'count': len(tag_objects)})
#
#     def post(self, request, *args, **kwargs):
#         form = TagForm(request.POST)
#         rio_user = api_models.RioUser.objects.filter(user=self.request.user).first()
#
#         if form.is_valid():
#             if form.cleaned_data.get('name').lower() in self.INVALID_NAMES:
#                 form.add_error('name', 'Prohibited name.')
#                 return JsonResponse({'status': 'failed', 'errors': form.errors})
#
#             # Make sure that tag does not use the same name as an existing tag, comm, or tag_set
#             tag = api_models.Tag.objects.filter(name__iexact=form.cleaned_data.get('name')).first()
#             tag_slugified = api_models.Tag.objects.filter(slug__iexact=slugify(form.cleaned_data.get('name'))).first()
#             comm_name_check = api_models.Community.objects.filter(name__iexact=form.cleaned_data.get('name')).first()
#             tag_set = api_models.TagSet.objects.filter(name__iexact=form.cleaned_data.get('name')).first()
#             if tag or tag_slugified or comm_name_check or tag_set:
#                 form.add_error('name', 'Conflicting tag, community or tagset name.')
#                 return JsonResponse({'status': 'failed', 'errors': form.errors})
#
#             community = api_models.Community.objects.filter(name__iexact=form.cleaned_data.get('community_name')).first()
#             if community is None:
#                 form.add_error('community_name', 'Community does not exist by that name.')
#             else:
#                 # Check if the user has access to view this community
#                 community_user = api_models.CommunityUser.objects.filter(community=community, user=rio_user).first()
#                 if community_user is None or community_user.banned:
#                     form.add_error('community_name', 'Community does not exist by that name.')
#                 else:
#                     if not community_user.admin:
#                         # Now check if the user has admin status to add a Tag
#                         form.add_error('community_name',
#                                        'You do not have permissions to create a tag for this community. '
#                                        'Please ask an admin.')
#             # All our checks are done, check if we have any errors
#             if form.errors:
#                 return JsonResponse({'status': 'failed', 'errors': form.errors})
#             else:
#                 # No errors, create our Tag
#                 form.cleaned_data['community'] = community
#                 form.cleaned_data.pop('community_name')
#                 tag = api_models.Tag.objects.create(**form.cleaned_data)
#                 return JsonResponse({'status': 'successful', 'tags': [tag.to_dict()]})
#         # Form had errors originally
#         return JsonResponse({'status': 'failed', 'errors': form.errors})
#
#
# class TagSet(APIView):
#     authentication_classes = [JWTAuthentication, TokenAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, *args, **kwargs):
#         tagset_objects = api_models.TagSet.objects.all()
#
#         if request.query_params:
#             query = Q()
#             for k, v in request.query_params.items():
#                 query &= Q(**{k: v})  # Build the AND query
#             tagset_objects = tagset_objects.filter(query)
#
#         tagset_objects = [i.to_dict() for i in tagset_objects]
#
#         if not request.data and not request.data.get('full_tags'):
#             for tagset in tagset_objects:
#                 tagset['tags'] = [{'id': i['id'], 'name': i['name']} for i in tagset['tags']]
#
#         return JsonResponse(
#             {
#                 'status': 'successful',
#                 'tagsets': tagset_objects,
#                 'count': len(tagset_objects)
#             }
#         )
#
#     def post(self, request, *args, **kwargs):
#         form = TagSetForm(request.POST)
#         rio_user = api_models.RioUser.objects.filter(user=self.request.user).first()
#
#         if form.is_valid():
#             # Check if name is unique
#             tag = api_models.Tag.objects.filter(name__iexact=form.cleaned_data.get('name')).first()
#             comm_name_check = api_models.Community.objects.filter(name__iexact=form.cleaned_data.get('name')).first()
#             tag_set = api_models.TagSet.objects.filter(name__iexact=form.cleaned_data.get('name')).first()
#             if tag or comm_name_check or tag_set:
#                 form.add_error('name', 'Conflicting tag, community or tagset name.')
#                 return JsonResponse({'status': 'failed', 'errors': form.errors})
#
#             community = api_models.Community.objects.filter(
#                 name__iexact=form.cleaned_data.get('community_name')).first()
#             if community is None:
#                 form.add_error('community_name', 'Community does not exist by that name.')
#             else:
#                 # Check if the user has access to view this community
#                 community_user = api_models.CommunityUser.objects.filter(community=community, user=rio_user).first()
#                 if community_user is None or community_user.banned:
#                     form.add_error('community_name', 'Community does not exist by that name.')
#                 else:
#                     if not community_user.admin:
#                         # Now check if the user has admin status to add a Tag
#                         form.add_error('community_name',
#                                        'You do not have permissions to create a tagset for this community. '
#                                        'Please ask an admin.')
#
#             # All our checks are done, check if we have any errors
#             if form.errors:
#                 return JsonResponse({'status': 'failed', 'errors': form.errors})
#             else:
#                 # No errors, create our Tagset
#                 form.cleaned_data['community'] = community
#                 form.cleaned_data.pop('community_name')
#                 tags_to_add = []
#                 for tag_id in form.cleaned_data['tags'].split(','):
#                     tag = api_models.Tag.objects.filter(id=tag_id).first()
#                     if tag.tag_type in ['Community', 'Competition']:
#                         form.add_error('tags', f'Tag with ID, {tag_id}, has an invalid tag type.')
#                         continue
#                     if tag is None:
#                         form.add_error('tags', f'Tag with ID, {tag_id}, does not exist.')
#                         continue
#                     tags_to_add.append(tag)
#
#                 form.cleaned_data.pop('tags')
#                 tagset = api_models.TagSet.objects.create(**form.cleaned_data)
#                 for tag in tags_to_add:
#                     tagset.tags.add(tag)
#                 tagset.save()
#                 return JsonResponse({'status': 'successful', 'tags': [tagset.to_dict()]})
#         else:
#             return JsonResponse({'status': 'failed', 'errors': form.errors})
#
# class PopulateDB(APIView):
#     authentication_classes = [TokenAuthentication, JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, *args, **kwargs):
#         return JsonResponse({'results': 'GET method not valid. Only POST.'})
#
#     def post(self, request, *args, **kwargs):
#
#         start_time = datetime.now(tz=UTC)
#
#         form = PopulateDBForm(request.data)
#
#         if not form.is_valid():
#             return JsonResponse({'results': 'Invalid data sent', 'errors': form.errors})
#
#         # Ignore game versions below 1.9.5
#         version_split = form.cleaned_data['version'].split('.')
#         if version_split[0] == '1' and version_split[1] <= '9' and int(version_split[2]) <= 4:
#             return JsonResponse({'results': 'Not accepting games from clients below 1.9.5'})
#
#         # Ignore game if it's a CPU game
#         if form.cleaned_data['home_player'] == "CPU" or form.cleaned_data['away_player'] == "CPU":
#             return JsonResponse({'results': 'Database does not accept CPU games'})
#
#         # Ensure both players actually exist as Rio Users
#         home_player = api_models.Token.objects.filter(key=form.cleaned_data['home_player']).first()
#         away_player = api_models.Token.objects.filter(key=form.cleaned_data['away_player']).first()
#         if home_player is None:
#             return JsonResponse({'results': 'Home player not found.'})
#         if away_player is None:
#             return JsonResponse({'results': 'Away player not found.'})
#
#         home_player = home_player.user.riouser
#         away_player = away_player.user.riouser
#
#         # Check if users are verified
#         if not home_player.verified:
#             return JsonResponse({'results': 'Home player not verified.'})
#         if not away_player.verified:
#             return JsonResponse({'results': 'Away player not verified.'})
#
#         # Detect invalid games
#         innings_selected = form.cleaned_data['innings_selected']
#         innings_played = form.cleaned_data['innings_played']
#         score_difference = abs(form.cleaned_data['home_score'] - form.cleaned_data['away_score'])
#         is_valid = False if innings_played < innings_selected and score_difference < 10 else True
#
#         if not is_valid:
#             return JsonResponse({'results': 'Invalid Game: Innings Played < Innings Selected & Score Difference < 10'})
#
#         # Validate the tagset ID
#         tag_set = TagSet.objects.filter(id=form.cleaned_data['tagset_id']).first()
#         if tag_set is None:
#             return JsonResponse({'results': f'Could not find tagset with id, {form.cleaned_data["tagset_id"]}'})
#
#         # Confirm that both users are community members for given TagSet
#         # Get TagSet obj to verify users
#
#         home_comm_user = api_models.CommunityUser.objects.filter(user=home_player, community=tag_set.community).first()
#         away_comm_user = api_models.CommunityUser.objects.filter(user=away_player, community=tag_set.community).first()
#
#         if home_comm_user is None or away_comm_user is None:
#             return JsonResponse({'results': 'One or both users are not part of the community for this TagSet.'})
#
#         # TODO Look into removing this step. GameID SHOULD be guaranteed by checking in ongoing_games now
#         # Reroll game id until unique one is found
#         unique_id = False
#         game_id = int(form.cleaned_data['game_id'].replace(',', ''), 16)
#         while not unique_id:
#             game = api_models.Game.objects.filter(game_id=game_id).first()
#             if game is None:
#                 unique_id = True
#             else:
#                 game_id = random.getrandbits(32)
#
#         # Delete ongoing game row once game is submitted
#         api_models.OngoingGame.objects.filter(game_id=game_id).delete()
#
#         game = api_models.Game.objects.create(
#             game_id=game_id,
#             away_player=away_player,
#             home_player=home_player,
#             date_time_start=int(form.cleaned_data['date_start']),
#             date_time_end=int(form.cleaned_data['date_end']),
#             netplay=form.cleaned_data['netplay'],
#             stadium_id=form.cleaned_data['stadium_id'],
#             away_score=form.cleaned_data['away_score'],
#             home_score=form.cleaned_data['home_score'],
#             innings_selected=form.cleaned_data['innings_selected'],
#             innings_played=form.cleaned_data['innings_played'],
#             valid=is_valid,
#             average_ping=form.cleaned_data['average_ping'],
#             lag_spikes=form.cleaned_data['lag_spikes'],
#             version=form.cleaned_data['version'],
#         )
#         if not form.cleaned_data['quitter']:
#             game.quitter = form.cleaned_data['quitter']
#             game.save()
#
#         end_time = datetime.now(tz=UTC)
#         elapsed_time = (end_time - start_time).total_seconds()
#
#         return JsonResponse(
#             {
#                 'results': 'Game successfully uploaded!',
#                 'start_time': start_time,
#                 'end_time': end_time,
#                 'elapsed_time': f'{elapsed_time * 60} seconds',
#                 'game_id': game.id
#             }
#         )
