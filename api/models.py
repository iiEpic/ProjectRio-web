from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class ApiKey(models.Model):
    api_key = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_created=True, auto_now=True)
    pings_daily = models.IntegerField(default=1)
    pings_weekly = models.IntegerField(default=7)
    last_ping_date = models.DateTimeField(blank=True, null=True)
    total_pings = models.IntegerField(default=0)

    def __str__(self):
        return self.api_key


class ChemistryTable(models.Model):
    mario = models.IntegerField(default=0)
    luigi = models.IntegerField(default=0)
    dk = models.IntegerField(default=0)
    peach = models.IntegerField(default=0)
    daisy = models.IntegerField(default=0)
    yoshi = models.IntegerField(default=0)
    diddy = models.IntegerField(default=0)
    baby_mario = models.IntegerField(default=0)
    baby_luigi = models.IntegerField(default=0)
    bowser = models.IntegerField(default=0)
    wario = models.IntegerField(default=0)
    waluigi = models.IntegerField(default=0)
    koopa_r = models.IntegerField(default=0)
    toad_r = models.IntegerField(default=0)
    boo = models.IntegerField(default=0)
    toadette = models.IntegerField(default=0)
    shy_guy_r = models.IntegerField(default=0)
    birdo = models.IntegerField(default=0)
    monty = models.IntegerField(default=0)
    bowser_jr = models.IntegerField(default=0)
    paratroopa_r = models.IntegerField(default=0)
    pianta_b = models.IntegerField(default=0)
    pianta_r = models.IntegerField(default=0)
    pianta_y = models.IntegerField(default=0)
    noki_b = models.IntegerField(default=0)
    noki_r = models.IntegerField(default=0)
    noki_g = models.IntegerField(default=0)
    bro_h = models.IntegerField(default=0)
    toadsworth = models.IntegerField(default=0)
    toad_b = models.IntegerField(default=0)
    toad_y = models.IntegerField(default=0)
    toad_g = models.IntegerField(default=0)
    toad_p = models.IntegerField(default=0)
    magikoopa_b = models.IntegerField(default=0)
    magikoopa_r = models.IntegerField(default=0)
    magikoopa_g = models.IntegerField(default=0)
    magikoopa_y = models.IntegerField(default=0)
    king_boo = models.IntegerField(default=0)
    petey = models.IntegerField(default=0)
    dixie = models.IntegerField(default=0)
    goomba = models.IntegerField(default=0)
    paragoomba = models.IntegerField(default=0)
    koopa_g = models.IntegerField(default=0)
    paratroopa_g = models.IntegerField(default=0)
    shy_guy_b = models.IntegerField(default=0)
    shy_guy_y = models.IntegerField(default=0)
    shy_guy_g = models.IntegerField(default=0)
    shy_guy_bk = models.IntegerField(default=0)
    dry_bones_gy = models.IntegerField(default=0)
    dry_bones_g = models.IntegerField(default=0)
    dry_bones_r = models.IntegerField(default=0)
    dry_bones_b = models.IntegerField(default=0)
    bro_f = models.IntegerField(default=0)
    bro_b = models.IntegerField(default=0)


class Character(models.Model):
    chemistry_table = models.ForeignKey(ChemistryTable, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=16)
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


class UserGroup(models.Model):
    daily_limit = models.IntegerField(default=0)
    weekly_limit = models.IntegerField(default=0)
    sponsor_limit = models.IntegerField(default=0)
    name = models.CharField(max_length=32, unique=True)
    desc = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class RioUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.ForeignKey(ApiKey, blank=True, null=True, on_delete=models.CASCADE)
    user_group = models.ManyToManyField(UserGroup, blank=True)
    rio_key = models.CharField(max_length=50, unique=True, blank=True, null=True)
    active_url = models.CharField(max_length=50, unique=True, blank=True, null=True)
    private = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.user.username

    def username(self):
        return self.user.username


class Community(models.Model):
    name = models.CharField(max_length=32, unique=True)
    sponsor = models.ForeignKey(RioUser, null=True, on_delete=models.CASCADE)
    community_type = models.CharField(max_length=16, help_text='Season, League, or Tournament')
    private = models.BooleanField(default=True)
    active_tag_set_limit = models.IntegerField(default=0)
    active_url = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    date_created = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.pk,
            'name': self.name,
            'sponsor': self.sponsor.username(),
            'sponsor_id': self.sponsor.user.pk,
            'community_type': self.community_type,
            'private': self.private,
            'active_tag_set_limit': self.active_tag_set_limit,
            'active_url': self.active_url,
            'description': self.description,
            'date_created': self.date_created
        }


class CommunityUser(models.Model):
    user = models.ForeignKey(RioUser, null=False, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, null=False, on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    invited = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    banned = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_created=True, auto_now=True)

    def to_json(self):
        return {
            'id': self.pk,
            'user': self.user.username(),
            'user_id': self.user.pk,
            'community': self.community.name,
            'community_id': self.community.pk,
            'admin': self.admin,
            'invited': self.invited,
            'active': self.active,
            'banned': self.banned,
            'date_joined': self.date_joined
        }


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    tag_type = models.CharField(max_length=16)
    desc = models.CharField(max_length=300)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.pk,
            'name': self.name,
            'type': self.tag_type,
            'desc': self.desc,
            'active': self.active,
            'date_created': self.date_created
        }


class TagSet(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    name = models.CharField(max_length=120, unique=True)
    type = models.CharField(max_length=120)  # Season, league, tournament.
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.pk,
            'name': self.name,
            'type': self.type,
            'community': self.community.name,
            'community_id': self.community.pk,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'tags': [i.to_json() for i in self.tags.all()],
        }


class GeckoCodeTag(models.Model):
    tag = models.ForeignKey(Tag, null=False, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    code = models.TextField(blank=True)

    def to_json(self):
        return {
            'tag_id': self.tag.pk,
            'code': self.code,
            'description': self.description
        }


class OngoingGame(models.Model):
    date_time_start = models.DateTimeField()
    stadium_id = models.IntegerField(default=0)
    away_player = models.ForeignKey(RioUser, null=False, on_delete=models.CASCADE, related_name='ongoing_away_player')
    home_player = models.ForeignKey(RioUser, null=False, on_delete=models.CASCADE, related_name='ongoing_home_player')
    tag_set = models.ForeignKey(TagSet, null=False, on_delete=models.CASCADE)
    away_captain = models.IntegerField(default=0)
    home_captain = models.IntegerField(default=0)
    away_roster_0_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='away_roster_0_char')
    away_roster_1_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='away_roster_1_char')
    away_roster_2_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='away_roster_2_char')
    away_roster_3_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='away_roster_3_char')
    away_roster_4_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='away_roster_4_char')
    away_roster_5_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='away_roster_5_char')
    away_roster_6_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='away_roster_6_char')
    away_roster_7_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='away_roster_7_char')
    away_roster_8_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='away_roster_8_char')
    home_roster_0_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='home_roster_0_char')
    home_roster_1_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='home_roster_1_char')
    home_roster_2_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='home_roster_2_char')
    home_roster_3_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='home_roster_3_char')
    home_roster_4_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='home_roster_4_char')
    home_roster_5_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='home_roster_5_char')
    home_roster_6_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='home_roster_6_char')
    home_roster_7_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='home_roster_7_char')
    home_roster_8_char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE, related_name='home_roster_8_char')
    current_inning = models.IntegerField(default=0)
    current_half_inning = models.IntegerField(default=0)
    current_away_score = models.IntegerField(default=0)
    current_home_score = models.IntegerField(default=0)
    current_away_stars = models.IntegerField(default=0)
    current_home_stars = models.IntegerField(default=0)
    current_outs = models.IntegerField(default=0)
    current_runner_1b = models.BooleanField(default=False)
    current_runner_2b = models.BooleanField(default=False)
    current_runner_3b = models.BooleanField(default=False)
    batter_roster_loc = models.IntegerField(default=0)
    pitcher_roster_loc = models.IntegerField(default=0)


class Game(models.Model):
    away_player = models.ForeignKey(RioUser, null=False, on_delete=models.CASCADE, related_name='game_away_player')
    home_player = models.ForeignKey(RioUser, null=False, on_delete=models.CASCADE, related_name='game_home_player')
    date_time_start = models.DateTimeField()
    date_time_end = models.DateTimeField()
    ranked = models.BooleanField(default=False)
    netplay = models.BooleanField(default=True)
    stadium_id = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    home_score = models.IntegerField(default=0)
    innings_selected = models.IntegerField(default=3)
    innings_played = models.IntegerField(default=3)
    quitter = models.ForeignKey(RioUser, blank=True, null=True, on_delete=models.CASCADE, related_name='quitter_player')
    valid = models.BooleanField(default=True)
    average_ping = models.IntegerField(default=0)
    lag_spikes = models.IntegerField(default=0)
    version = models.CharField(max_length=50)


class CharacterPositionSummary(models.Model):
    pitches_at_p = models.IntegerField(default=0)
    pitches_at_c = models.IntegerField(default=0)
    pitches_at_1b = models.IntegerField(default=0)
    pitches_at_2b = models.IntegerField(default=0)
    pitches_at_3b = models.IntegerField(default=0)
    pitches_at_ss = models.IntegerField(default=0)
    pitches_at_lf = models.IntegerField(default=0)
    pitches_at_cf = models.IntegerField(default=0)
    pitches_at_rf = models.IntegerField(default=0)
    batter_outs_at_p = models.IntegerField(default=0)
    batter_outs_at_c = models.IntegerField(default=0)
    batter_outs_at_1b = models.IntegerField(default=0)
    batter_outs_at_2b = models.IntegerField(default=0)
    batter_outs_at_3b = models.IntegerField(default=0)
    batter_outs_at_ss = models.IntegerField(default=0)
    batter_outs_at_lf = models.IntegerField(default=0)
    batter_outs_at_cf = models.IntegerField(default=0)
    batter_outs_at_rf = models.IntegerField(default=0)
    outs_at_p = models.IntegerField(default=0)
    outs_at_c = models.IntegerField(default=0)
    outs_at_1b = models.IntegerField(default=0)
    outs_at_2b = models.IntegerField(default=0)
    outs_at_3b = models.IntegerField(default=0)
    outs_at_ss = models.IntegerField(default=0)
    outs_at_lf = models.IntegerField(default=0)
    outs_at_cf = models.IntegerField(default=0)
    outs_at_rf = models.IntegerField(default=0)


class CharacterGameSummary(models.Model):
    game = models.ForeignKey(Game, null=False, on_delete=models.CASCADE)
    char = models.ForeignKey(Character, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(RioUser, null=False, on_delete=models.CASCADE)
    character_position_summary = models.ForeignKey(CharacterPositionSummary, null=False, on_delete=models.CASCADE)
    team_id = models.IntegerField(default=0)
    roster_loc = models.IntegerField(default=0)  # 0-8
    captain = models.BooleanField(default=False)
    superstar = models.BooleanField(default=False)
    fielding_hand = models.BooleanField(default=False)
    batting_hand = models.BooleanField(default=False)
    #Defensive Stats
    batters_faced = models.IntegerField(default=0)
    runs_allowed = models.IntegerField(default=0)
    earned_runs = models.IntegerField(default=0)
    batters_walked = models.IntegerField(default=0)
    batters_hit = models.IntegerField(default=0)
    hits_allowed = models.IntegerField(default=0)
    homeruns_allowed = models.IntegerField(default=0)
    pitches_thrown = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)
    was_pitcher = models.IntegerField(default=0)
    strikeouts_pitched = models.IntegerField(default=0)
    star_pitches_thrown = models.IntegerField(default=0)
    big_plays = models.IntegerField(default=0)
    outs_pitched = models.IntegerField(default=0)
    #Offensive Stats
    at_bats = models.IntegerField(default=0)
    plate_appearances = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    singles = models.IntegerField(default=0)
    doubles = models.IntegerField(default=0)
    triples = models.IntegerField(default=0)
    homeruns = models.IntegerField(default=0)
    successful_bunts = models.IntegerField(default=0)
    sac_flys = models.IntegerField(default=0)
    strikeouts = models.IntegerField(default=0)
    walks_bb = models.IntegerField(default=0)
    walks_hit = models.IntegerField(default=0)
    rbi = models.IntegerField(default=0)
    bases_stolen = models.IntegerField(default=0)
    star_hits = models.IntegerField(default=0)
    #Star tracking (Not in JSON. Calculated in populate_db)
    offensive_star_swings = models.IntegerField(default=0)
    offensive_stars_used = models.IntegerField(default=0)
    offensive_stars_put_in_play = models.IntegerField(default=0)
    offensive_star_successes = models.IntegerField(default=0)
    offensive_star_chances = models.IntegerField(default=0)
    offensive_star_chances_won = models.IntegerField(default=0)
    defensive_star_pitches = models.IntegerField(default=0)
    defensive_stars_used = models.IntegerField(default=0)
    defensive_star_successes = models.IntegerField(default=0)
    defensive_star_chances = models.IntegerField(default=0)
    defensive_star_chances_won = models.IntegerField(default=0)


class Runner(models.Model):
    runner_character_game_summary = models.ForeignKey(CharacterGameSummary, null=False, on_delete=models.CASCADE)
    initial_base = models.IntegerField(default=0)
    result_base = models.IntegerField(default=0)
    out_type = models.IntegerField(default=0)
    out_location = models.IntegerField(default=0)
    steal = models.IntegerField(default=0)


class FieldingSummary(models.Model):
    fielder_character_game_summary = models.ForeignKey(CharacterGameSummary, null=False, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    action = models.IntegerField(default=0)
    jump = models.IntegerField(default=0)
    bobble = models.IntegerField(default=0)
    swap = models.BooleanField(default=False)
    manual_select = models.IntegerField(default=0)
    fielder_x_pos = models.FloatField(default=0.0)
    fielder_y_pos = models.FloatField(default=0.0)
    fielder_z_pos = models.FloatField(default=0.0)


class ContactSummary(models.Model):
    fielding_summary = models.ForeignKey(FieldingSummary, null=True, on_delete=models.CASCADE)
    type_of_contact = models.IntegerField(default=0)
    charge_power_up = models.FloatField(default=0.0)
    charge_power_down = models.FloatField(default=0.0)
    star_swing_five_star = models.IntegerField(default=0)
    input_direction = models.IntegerField(default=0)
    input_direction_stick = models.IntegerField(default=0)
    frame_of_swing_upon_contact = models.IntegerField(default=0)
    ball_power = models.IntegerField(default=0)
    ball_horiz_angle = models.IntegerField(default=0)
    ball_vert_angle = models.IntegerField(default=0)
    contact_absolute = models.FloatField(default=0.0)
    contact_quality = models.FloatField(default=0.0)
    rng1 = models.FloatField(default=0.0)
    rng2 = models.FloatField(default=0.0)
    rng3 = models.FloatField(default=0.0)
    ball_x_velocity = models.FloatField(default=0.0)
    ball_y_velocity = models.FloatField(default=0.0)
    ball_z_velocity = models.FloatField(default=0.0)
    ball_x_contact_pos = models.FloatField(default=0.0)
    ball_z_contact_pos = models.FloatField(default=0.0)
    ball_x_landing_pos = models.FloatField(default=0.0)
    ball_y_landing_pos = models.FloatField(default=0.0)
    ball_z_landing_pos = models.FloatField(default=0.0)
    ball_max_height = models.FloatField(default=0.0)
    ball_hang_time = models.FloatField(default=0.0)
    primary_result = models.IntegerField(default=0)
    secondary_result = models.IntegerField(default=0)


class PitchSummary(models.Model):
    contact_summary = models.ForeignKey(ContactSummary, null=True, on_delete=models.CASCADE)
    pitch_type = models.IntegerField(default=0)
    charge_pitch_type = models.IntegerField(default=0)
    star_pitch = models.IntegerField(default=0)
    pitch_speed = models.IntegerField(default=0)
    d_ball = models.BooleanField(default=False)
    type_of_swing = models.IntegerField(default=0)
    ball_position_strikezone = models.IntegerField(default=0)
    in_strikezone = models.BooleanField(default=False)
    bat_x_contact_pos = models.FloatField(default=0.0)
    bat_z_contact_pos = models.FloatField(default=0.0)


class Event(models.Model):
    game = models.ForeignKey(Game, null=False, on_delete=models.CASCADE)
    pitcher = models.ForeignKey(CharacterGameSummary, null=False, on_delete=models.CASCADE, related_name='event_pitcher')  # Based on "Pitcher Roster Loc" in JSON
    batter = models.ForeignKey(CharacterGameSummary, null=False, on_delete=models.CASCADE, related_name='event_batter')
    catcher = models.ForeignKey(CharacterGameSummary, null=False, on_delete=models.CASCADE, related_name='event_catcher')
    runner_on_0 = models.ForeignKey(Runner, null=False, on_delete=models.CASCADE, related_name='event_runner_0')
    runner_on_1 = models.ForeignKey(Runner, null=True, on_delete=models.CASCADE, related_name='event_runner_1')
    runner_on_2 = models.ForeignKey(Runner, null=True, on_delete=models.CASCADE, related_name='event_runner_2')
    runner_on_3 = models.ForeignKey(Runner, null=True, on_delete=models.CASCADE, related_name='event_runner_3')
    pitch_summary = models.ForeignKey(PitchSummary, null=True, on_delete=models.CASCADE)
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


class Ladder(models.Model):
    tag_set = models.ForeignKey(TagSet, null=False, on_delete=models.CASCADE)
    community_user = models.ForeignKey(CommunityUser, null=False, on_delete=models.CASCADE)
    started_searching = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    rd = models.IntegerField(default=0)
    vol = models.FloatField(default=0.0)


class GameHistory(models.Model):
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
    tag_set = models.ForeignKey(TagSet, null=False, on_delete=models.CASCADE)
    winner_comm_user = models.ForeignKey(CommunityUser, null=False, on_delete=models.CASCADE, related_name='winner_comm_user')
    loser_comm_user = models.ForeignKey(CommunityUser, null=False, on_delete=models.CASCADE, related_name='loser_comm_user')
    winner_score = models.IntegerField(default=0)
    loser_score = models.IntegerField(default=0)
    winner_elo = models.IntegerField(default=0)
    loser_elo = models.IntegerField(default=0)
    winner_accept = models.BooleanField(default=True)
    loser_accept = models.BooleanField(null=True)
    admin_accept = models.BooleanField(null=True)
    date_created = models.IntegerField(null=True)
