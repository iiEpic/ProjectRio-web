from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import rest_framework.authtoken.models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone
import enum
import re


class Token(rest_framework.authtoken.models.Token):
    key = models.CharField(_("Key"), max_length=50, db_index=True, unique=True)
    user = models.OneToOneField(  # Changed to OneToOneField
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User"), unique=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    pings_daily = models.IntegerField(default=1)
    pings_weekly = models.IntegerField(default=7)
    last_ping_date = models.DateTimeField(blank=True, null=True)
    total_pings = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}"


@receiver(post_save, sender=User)
def create_auth_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserGroup(models.Model):
    name = models.CharField(max_length=32, unique=True, db_index=True)
    slug = models.SlugField(max_length=32, unique=True, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)
    sponsor_limit = models.IntegerField(default=0)
    daily_limit = models.IntegerField(default=0)
    weekly_limit = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['daily_limit']),
            models.Index(fields=['weekly_limit']),
            models.Index(fields=['sponsor_limit']),
        ]

    def __str__(self):
        return f"{self.name}"


@receiver(pre_save, sender=UserGroup)
def usergroup_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, db_index=True)
    user_group = models.ManyToManyField(UserGroup, blank=True)
    active_url = models.CharField(max_length=50, unique=True, blank=True, null=True, db_index=True)
    private = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['private']),
            models.Index(fields=['verified']),
        ]

    def __str__(self):
        return f"Profile for {self.user.username}"


class Character(models.Model):
    name = models.CharField(max_length=16)
    slug = models.SlugField(max_length=16, unique=True, blank=True, null=True)
    starting_addr = models.CharField(max_length=16)
    curve_ball_speed = models.IntegerField(default=0)
    fast_ball_speed = models.IntegerField(default=0)
    curve = models.IntegerField(default=0)
    fielding_arm = models.IntegerField(default=0)
    batting_stance = models.IntegerField(default=0)
    nice_contact_spot_size = models.IntegerField(default=0)
    perfect_contact_spot_size = models.IntegerField(default=0)
    slap_hit_power = models.IntegerField(default=0)
    charge_hit_power = models.IntegerField(default=0)
    bunting = models.IntegerField(default=0)
    hit_trajectory_mpp = models.IntegerField(default=0)
    hit_trajectory_mhl = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    throwing_arm = models.IntegerField(default=0)
    character_class = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    captain = models.BooleanField(default=False)
    captain_star_hit_or_pitch = models.IntegerField(default=0)
    non_captain_star_swing = models.IntegerField(default=0)
    non_captain_star_pitch = models.IntegerField(default=0)
    batting_stat_bar = models.IntegerField(default=0)
    pitching_stat_bar = models.IntegerField(default=0)
    running_stat_bar = models.IntegerField(default=0)
    fielding_stat_bar = models.IntegerField(default=0)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Character)
def character_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


class CharacterChemistry(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name="compatibility")
    compatibility_values = models.JSONField(default=dict)

    def __str__(self):
        return f"Compatibility for {self.character.name}"


class Community(models.Model):
    COMMUNITY_TYPES = (
        ('official', 'Official'),
        ('unofficial', 'Unofficial'),
    )

    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True, blank=True, null=True)
    sponsor = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="sponsored_communities")
    community_type = models.CharField(max_length=16, choices=COMMUNITY_TYPES)
    private = models.BooleanField(default=True)
    active_tag_set_limit = models.IntegerField(default=5)
    active_url = models.CharField(max_length=50, blank=True, null=True, unique=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, through='CommunityUser', related_name='communities')

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Community)
def community_pre_save(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Role)
def role_pre_save(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)


class CommunityUserStatus(enum.Enum):
    INVITED = 'invited'
    ACTIVE = 'active'
    BANNED = 'banned'


class CommunityUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=1)
    status = models.CharField(
        max_length=10,
        choices=[(tag.value, tag.name) for tag in CommunityUserStatus],
        default=CommunityUserStatus.INVITED.value,
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.community.name} as {self.role.name}"


class Tag(models.Model):
    TAG_TYPES = (
        ('component', 'Component'),
        ('competition', 'Competition'),
        ('community', 'Community'),
        ('client_code', 'Client Code'),
        ('gecko_code', 'Gecko Code'),
        ('test', 'Test'),
    )

    name = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, db_index=True)
    tag_type = models.CharField(max_length=16, choices=TAG_TYPES, db_index=True)
    community = models.ForeignKey('Community', on_delete=models.CASCADE, blank=True, null=True, db_index=True)

    description = models.CharField(max_length=300, blank=True, null=True)
    gecko_code = models.TextField(blank=True, null=True)
    gecko_code_desc = models.CharField(blank=True, null=True, max_length=255)

    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def display_gecko_code(self):
        formatted_string = re.sub(r"([a-fA-F0-9]{8} [a-fA-F0-9]{8})", r"\1<br/>", self.gecko_code)
        return formatted_string


@receiver(pre_save, sender=Tag)
def tag_pre_save(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)


class TagSet(models.Model):
    TAGSET_TYPES = (
        ('season', 'Season'),
        ('league', 'League'),
        ('tournament', 'Tournament'),
    )

    community = models.ForeignKey('Community', on_delete=models.CASCADE, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True)
    name = models.CharField(max_length=120, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    tagset_type = models.CharField(max_length=120, choices=TAGSET_TYPES, db_index=True)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)

    def __str__(self):
        return self.name

    def display_status(self):
        now = timezone.now()
        if self.start_date > now:
            return '<span class="badge rounded-pill text-bg-danger">Inactive</span>'
        elif self.start_date <= now <= self.end_date:
            return '<span class="badge rounded-pill text-bg-success">In-progress</span>'
        else:
            return '<span class="badge rounded-pill text-bg-danger">Inactive</span>'

    def get_status(self):
        now = timezone.now()
        if self.start_date > now:
            return 'Active'
        elif self.start_date <= now <= self.end_date:
            return 'Active'
        else:
            return 'Inactive'

    def display_alert(self):
        now = timezone.now()
        if self.start_date > now:
            return {'status': 'future', 'message': 'Gamemode scheduled for future dates', 'alert': 'primary'}
        elif self.start_date <= now <= self.end_date:
            return {'status': 'in-progress', 'message': 'Gamemode is currently in-progress', 'alert': 'success'}
        else:
            return {'status': 'inactive', 'message': 'Gamemode is no longer active', 'alert': 'danger'}


@receiver(pre_save, sender=TagSet)
def tagset_pre_save(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)


class Game(models.Model):
    GAME_STATUS = (
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('aborted', 'Aborted'),
    )

    game_id = models.IntegerField(unique=True)
    away_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='away_games')
    home_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='home_games')
    date_time_start = models.DateTimeField(default=timezone.now)
    date_time_end = models.DateTimeField(blank=True, null=True)
    ranked = models.BooleanField(default=False)
    netplay = models.BooleanField(default=True)
    stadium_id = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    home_score = models.IntegerField(default=0)
    innings_selected = models.IntegerField(default=3)
    innings_played = models.IntegerField(default=3)
    quitter = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='quit_games')
    valid = models.BooleanField(default=True)
    average_ping = models.IntegerField(default=0)
    lag_spikes = models.IntegerField(default=0)
    version = models.CharField(max_length=50)
    tag_set = models.ForeignKey('TagSet', null=True, on_delete=models.SET_NULL, blank=True)
    status = models.CharField(max_length=10, choices=GAME_STATUS, default='pending')
    current_inning = models.IntegerField(default=0)
    current_half_inning = models.IntegerField(default=0)
    current_away_stars = models.IntegerField(default=0)
    current_home_stars = models.IntegerField(default=0)
    current_outs = models.IntegerField(default=0)
    current_runner_1b = models.BooleanField(default=False)
    current_runner_2b = models.BooleanField(default=False)
    current_runner_3b = models.BooleanField(default=False)
    batter_roster_loc = models.IntegerField(default=0)
    pitcher_roster_loc = models.IntegerField(default=0)
    away_captain = models.ForeignKey('Character', null=True, on_delete=models.SET_NULL, related_name="away_captain")
    home_captain = models.ForeignKey('Character', null=True, on_delete=models.SET_NULL, related_name="home_captain")

    def __str__(self):
        return f"Game {self.game_id} - {self.away_player} vs {self.home_player}"


class GameRoster(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="rosters")
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    roster_location = models.IntegerField()
    is_home_team = models.BooleanField(default=False)

    class Meta:
        unique_together = ('game', 'roster_location', 'is_home_team')

    def __str__(self):
        team_str = "Home" if self.is_home_team else "Away"
        return f"{self.player.username} ({team_str}) - {self.character.name} in Game {self.game.game_id}, Roster Loc: {self.roster_location}"


class GameEventSummary(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team_id = models.IntegerField(default=0)
    roster_loc = models.IntegerField(default=0)
    captain = models.BooleanField(default=False)
    superstar = models.BooleanField(default=False)
    fielding_hand = models.BooleanField(default=False)
    batting_hand = models.BooleanField(default=False)
    position_stats = models.JSONField(default=dict)  # Stores position-specific stats
    offensive_stats = models.JSONField(default=dict)  # Offensive stats
    defensive_stats = models.JSONField(default=dict)  # Defensive stats
    runner_stats = models.JSONField(default=dict)  # Runner stats
    fielding_stats = models.JSONField(default=dict)  # Fielding stats
    contact_stats = models.JSONField(default=dict)  # Contact stats
    pitch_stats = models.JSONField(default=dict)  # Pitch stats
    star_stats = models.JSONField(default=dict)  # Star stats

    def __str__(self):
        return f"Summary for {self.user.username}, Game {self.game.game_id}, Character: {self.character.name}, Roster Loc: {self.roster_loc}"


class GameEvent(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    pitcher = models.ForeignKey(GameEventSummary, on_delete=models.CASCADE, related_name='event_pitcher')
    batter = models.ForeignKey(GameEventSummary, on_delete=models.CASCADE, related_name='event_batter')
    catcher = models.ForeignKey(GameEventSummary, on_delete=models.CASCADE, related_name='event_catcher')
    runners = models.ManyToManyField(GameEventSummary, related_name='event_runners')
    event_num = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    home_score = models.IntegerField(default=0)
    inning = models.IntegerField(default=0)
    half_inning = models.IntegerField(default=0)
    chem_links_ob = models.IntegerField(default=0)
    star_chance = models.IntegerField(default=0)
    away_stars = models.IntegerField(default=0)
    home_stars = models.IntegerField(default=0)
    pitcher_stamina = models.IntegerField(default=0)
    outs = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    strikes = models.IntegerField(default=0)
    result_num_of_outs = models.IntegerField(default=0)
    result_rbi = models.IntegerField(default=0)
    result_of_ab = models.IntegerField(default=0)
    winner_comm_user = models.ForeignKey('CommunityUser', null=True, on_delete=models.SET_NULL, related_name='winner_comm_user')
    loser_comm_user = models.ForeignKey('CommunityUser', null=True, on_delete=models.SET_NULL, related_name='loser_comm_user')
    winner_score = models.IntegerField(default=0)
    loser_score = models.IntegerField(default=0)
    winner_elo = models.IntegerField(default=0)
    loser_elo = models.IntegerField(default=0)
    winner_accept = models.BooleanField(default=True)
    loser_accept = models.BooleanField(null=True)
    admin_accept = models.BooleanField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.event_num} in Game {self.game.game_id}, Inning: {self.inning}.{self.half_inning}"


class Ladder(models.Model):
    tag_set = models.ForeignKey('TagSet', on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    started_searching = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)
    rd = models.IntegerField(default=0)
    vol = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('tag_set', 'user') #A user only has one ladder per tag set.

    def __str__(self):
        return f"{self.user.username} - {self.tag_set.name} Ladder"
