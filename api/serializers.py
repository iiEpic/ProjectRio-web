from rest_framework import serializers
from .models import (
    Token, UserGroup, UserProfile, Character, CharacterChemistry,
    Community, Role, CommunityUser, Tag, TagSet, Game, GameRoster,
    GameEventSummary, GameEvent, Ladder
)


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key', 'user', 'date_created', 'pings_daily', 'pings_weekly', 'last_ping_date', 'total_pings']


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['id', 'name', 'description', 'sponsor_limit', 'daily_limit', 'weekly_limit']


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_group = serializers.StringRelatedField(many=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'user_group', 'active_url', 'private', 'verified', 'date_created']


class CharacterSerializer(serializers.ModelSerializer):
    captain = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = [
            'id', 'name', 'starting_addr', 'curve_ball_speed', 'fast_ball_speed', 'curve', 'fielding_arm',
            'batting_stance', 'nice_contact_spot_size', 'perfect_contact_spot_size', 'slap_hit_power',
            'charge_hit_power', 'bunting', 'hit_trajectory_mpp', 'hit_trajectory_mhl', 'speed', 'throwing_arm',
            'character_class', 'weight', 'captain', 'captain_star_hit_or_pitch', 'non_captain_star_swing',
            'non_captain_star_pitch', 'batting_stat_bar', 'pitching_stat_bar', 'running_stat_bar', 'fielding_stat_bar'
        ]

    def get_captain(self, obj):
        return 'True' if obj.captain else 'False'


class CharacterChemistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterChemistry
        fields = ['id', 'character', 'compatibility_values']


class CommunitySerializer(serializers.ModelSerializer):
    sponsor = serializers.StringRelatedField()
    members = serializers.StringRelatedField(many=True)
    class Meta:
        model = Community
        fields = ['id', 'name', 'slug', 'sponsor', 'community_type', 'private', 'active_tag_set_limit', 'active_url', 'description', 'date_created', 'members']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class CommunityUserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    community = serializers.StringRelatedField()
    role = serializers.StringRelatedField()

    class Meta:
        model = CommunityUser
        fields = ['id', 'user', 'community', 'role', 'status', 'date_joined']


class TagSerializer(serializers.ModelSerializer):
    community = serializers.StringRelatedField()
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'tag_type', 'community', 'description', 'gecko_code', 'gecko_code_desc', 'active', 'date_created', 'last_modified']


class TagSetSerializer(serializers.ModelSerializer):
    community = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    class Meta:
        model = TagSet
        fields = ['id', 'community', 'tags', 'name', 'tagset_type', 'start_date', 'end_date']


class GameSerializer(serializers.ModelSerializer):
    away_player = serializers.StringRelatedField()
    home_player = serializers.StringRelatedField()
    quitter = serializers.StringRelatedField()
    tag_set = serializers.StringRelatedField()
    away_captain = serializers.StringRelatedField()
    home_captain = serializers.StringRelatedField()

    class Meta:
        model = Game
        fields = [
            'id', 'game_id', 'away_player', 'home_player', 'date_time_start', 'date_time_end', 'ranked',
            'netplay', 'stadium_id', 'away_score', 'home_score', 'innings_selected', 'innings_played',
            'quitter', 'valid', 'average_ping', 'lag_spikes', 'version', 'tag_set', 'status',
            'current_inning', 'current_half_inning', 'current_away_stars', 'current_home_stars',
            'current_outs', 'current_runner_1b', 'current_runner_2b', 'current_runner_3b',
            'batter_roster_loc', 'pitcher_roster_loc', 'away_captain', 'home_captain'
        ]


class GameRosterSerializer(serializers.ModelSerializer):
    game = serializers.StringRelatedField()
    character = serializers.StringRelatedField()
    player = serializers.StringRelatedField()

    class Meta:
        model = GameRoster
        fields = ['id', 'game', 'character', 'player', 'roster_location', 'is_home_team']


class GameEventSummarySerializer(serializers.ModelSerializer):
    game = serializers.StringRelatedField()
    character = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = GameEventSummary
        fields = ['id', 'game', 'character', 'user', 'team_id', 'roster_loc', 'captain', 'superstar', 'fielding_hand', 'batting_hand', 'position_stats', 'offensive_stats', 'defensive_stats', 'runner_stats', 'fielding_stats', 'contact_stats', 'pitch_stats', 'star_stats']


class GameEventSerializer(serializers.ModelSerializer):
    game = serializers.StringRelatedField()
    pitcher = serializers.StringRelatedField()
    batter = serializers.StringRelatedField()
    catcher = serializers.StringRelatedField()
    runners = serializers.StringRelatedField(many=True)
    winner_comm_user = serializers.StringRelatedField()
    loser_comm_user = serializers.StringRelatedField()

    class Meta:
        model = GameEvent
        fields = ['id', 'game', 'pitcher', 'batter', 'catcher', 'runners', 'event_num', 'away_score', 'home_score', 'inning', 'half_inning', 'chem_links_ob', 'star_chance', 'away_stars', 'home_stars', 'pitcher_stamina', 'outs', 'balls', 'strikes', 'result_num_of_outs', 'result_rbi', 'result_of_ab', 'winner_comm_user', 'loser_comm_user', 'winner_score', 'loser_score', 'winner_elo', 'loser_elo', 'winner_accept', 'loser_accept', 'admin_accept', 'date_created']


class LadderSerializer(serializers.ModelSerializer):
    tag_set = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Ladder
        fields = ['id', 'tag_set', 'user', 'started_searching', 'rating', 'rd', 'vol']