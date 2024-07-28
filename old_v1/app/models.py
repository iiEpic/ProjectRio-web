from . import db, bc
from flask_login import UserMixin
from .util import *
import time
import secrets

class Character(db.Model):
    char_id = db.Column(db.Integer, primary_key=True)
    chemistry_table_id = db.Column(db.ForeignKey('chemistry_table.id'), nullable = False)
    name = db.Column(db.String(16))
    name_lowercase = db.Column(db.String(16))
    starting_addr = db.Column(db.String(16))
    curve_ball_speed = db.Column(db.Integer)
    fast_ball_speed = db.Column(db.Integer)
    curve = db.Column(db.Integer)
    fielding_arm = db.Column(db.Integer)
    batting_stance = db.Column(db.Integer)
    nice_contact_spot_size = db.Column(db.Integer)
    perfect_contact_spot_size = db.Column(db.Integer)
    slap_hit_power = db.Column(db.Integer)
    charge_hit_power = db.Column(db.Integer)
    bunting = db.Column(db.Integer)
    hit_trajectory_mpp = db.Column(db.Integer)
    hit_trajectory_mhl = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    throwing_arm = db.Column(db.Integer)
    character_class = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    captain = db.Column(db.Integer)
    captain_star_hit_or_pitch = db.Column(db.Integer)
    non_captain_star_swing = db.Column(db.Integer)
    non_captain_star_pitch = db.Column(db.Integer)
    batting_stat_bar = db.Column(db.Integer)
    pitching_stat_bar = db.Column(db.Integer)
    running_stat_bar = db.Column(db.Integer)
    fielding_stat_bar = db.Column(db.Integer)
    
    character_game_summary = db.relationship('CharacterGameSummary', backref = 'character_game_summary_from_character')

    def to_dict(self):
        return {
            'char_id': self.char_id,
            'chemistry_table_id': self.chemistry_table_id,
            'name': self.name,
            'starting_addr': self.starting_addr,
            'curve_ball_speed': self.curve_ball_speed,
            'fast_ball_speed': self.fast_ball_speed,
            'curve': self.curve,
            'fielding_arm': self.fielding_arm,
            'batting_stance': self.batting_stance,
            'nice_contact_spot_size': self.nice_contact_spot_size,
            'perfect_contact_spot_size': self.perfect_contact_spot_size,
            'slap_hit_power': self.slap_hit_power,
            'charge_hit_power': self.charge_hit_power,
            'bunting': self.bunting,
            'hit_trajectory_mpp': self.hit_trajectory_mpp,
            'hit_trajectory_mhl': self.hit_trajectory_mhl,
            'speed': self.speed,
            'throwing_arm': self.throwing_arm,
            'character_class': self.character_class,
            'weight': self.weight,
            'captain': 'True' if self.captain == 1 else 'False',
            'captain_star_hit_or_pitch': self.captain_star_hit_or_pitch,
            'non_captain_star_swing': self.non_captain_star_swing,
            'non_captain_star_pitch': self.non_captain_star_pitch,
            'batting_stat_bar': self.batting_stat_bar,
            'pitching_stat_bar': self.pitching_stat_bar,
            'running_stat_bar': self.running_stat_bar,
            'fielding_stat_bar': self.fielding_stat_bar,
        }

class ChemistryTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mario = db.Column(db.Integer)
    luigi = db.Column(db.Integer)
    dk = db.Column(db.Integer)
    diddy = db.Column(db.Integer)
    peach = db.Column(db.Integer)
    daisy = db.Column(db.Integer)
    yoshi = db.Column(db.Integer)
    baby_mario = db.Column(db.Integer)
    baby_luigi = db.Column(db.Integer)
    bowser = db.Column(db.Integer)
    wario = db.Column(db.Integer)
    waluigi = db.Column(db.Integer)
    koopa_r = db.Column(db.Integer)
    toad_r = db.Column(db.Integer)
    boo = db.Column(db.Integer)
    toadette = db.Column(db.Integer)
    shy_guy_r = db.Column(db.Integer)
    birdo = db.Column(db.Integer)
    monty = db.Column(db.Integer)
    bowser_jr = db.Column(db.Integer)
    paratroopa_r = db.Column(db.Integer)
    pianta_b = db.Column(db.Integer)
    pianta_r = db.Column(db.Integer)
    pianta_y = db.Column(db.Integer)
    noki_b = db.Column(db.Integer)
    noki_r = db.Column(db.Integer)
    noki_g = db.Column(db.Integer)
    bro_h = db.Column(db.Integer)
    toadsworth = db.Column(db.Integer)
    toad_b = db.Column(db.Integer)
    toad_y = db.Column(db.Integer)
    toad_g = db.Column(db.Integer)
    toad_p = db.Column(db.Integer)
    magikoopa_b = db.Column(db.Integer)
    magikoopa_r = db.Column(db.Integer)
    magikoopa_g = db.Column(db.Integer)
    magikoopa_y = db.Column(db.Integer)
    king_boo = db.Column(db.Integer)
    petey = db.Column(db.Integer)
    dixie = db.Column(db.Integer)
    goomba = db.Column(db.Integer)
    paragoomba = db.Column(db.Integer)
    koopa_g = db.Column(db.Integer)
    paratroopa_g = db.Column(db.Integer)
    shy_guy_b = db.Column(db.Integer)
    shy_guy_y = db.Column(db.Integer)
    shy_guy_g = db.Column(db.Integer)
    shy_guy_bk = db.Column(db.Integer)
    dry_bones_gy = db.Column(db.Integer)
    dry_bones_g = db.Column(db.Integer)
    dry_bones_r = db.Column(db.Integer)
    dry_bones_b = db.Column(db.Integer)
    bro_f = db.Column(db.Integer)
    bro_b = db.Column(db.Integer)

    character = db.relationship('Character', backref = 'character')


class RioUser(db.Model, UserMixin):
    id       = db.Column(db.Integer, primary_key=True)
    api_key_id = db.Column(db.ForeignKey('api_key.id'), nullable=True)
    username = db.Column(db.String(64),  unique = True)
    username_lowercase = db.Column(db.String(64), unique = True)
    email    = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(500))
    rio_key  = db.Column(db.String(50), unique = True)
    private = db.Column(db.Boolean)
    verified = db.Column(db.Boolean)
    active_url = db.Column(db.String(50), unique = True)
    date_created = db.Column(db.Integer)

    community_user = db.relationship('CommunityUser', backref='rio_user')
    character_game_summaries = db.relationship('CharacterGameSummary', backref = 'rio_user', lazy = 'dynamic')
    away_games = db.relationship('Game', foreign_keys = 'Game.away_player_id', backref = 'games_as_away_player')
    home_games = db.relationship('Game', foreign_keys = 'Game.home_player_id', backref = 'games_as_home_player')

    user_group_user = db.relationship('UserGroupUser', backref='user_from_ugu')

    def __init__(self, in_username, in_email, in_password):
        self.username = in_username
        self.username_lowercase = lower_and_remove_nonalphanumeric(in_username)
        self.email    = in_email
        self.password = bc.generate_password_hash(in_password)
        self.rio_key  = secrets.token_urlsafe(32)
        self.private = True
        self.verified = False
        self.active_url = secrets.token_urlsafe(32)
        self.date_created = int(time.time())

class UserGroupUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('rio_user.id'), nullable=False)
    user_group_id = db.Column(db.ForeignKey('user_group.id'), nullable=False)
    
    def __init__(self, user_id, user_group_id):
        self.user_id = user_id,
        self.user_group_id = user_group_id

class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    daily_limit = db.Column(db.Integer)
    weekly_limit = db.Column(db.Integer)
    sponsor_limit = db.Column(db.Integer)
    name = db.Column(db.String(32), unique=True)
    name_lowercase = db.Column(db.String(32), unique=True)
    desc = db.Column(db.String(128))
    
    user_group_user = db.relationship('UserGroupUser', backref='user_group_from_ugu')

    def __init__(self, in_group_name, in_daily_limit, in_weekly_limit, in_sponsor_limit):
        self.name = in_group_name,
        self.name_lowercase = lower_and_remove_nonalphanumeric(in_group_name)
        self.daily_limit = in_daily_limit
        self.weekly_limit = in_weekly_limit
        self.sponsor_limit = in_sponsor_limit

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    name_lowercase = db.Column(db.String(32), unique=True)    
    sponsor_id = db.Column(db.Integer, db.ForeignKey('rio_user.id'), nullable=True)
    comm_type = db.Column(db.String(16))
    private = db.Column(db.Boolean)
    active_tag_set_limit = db.Column(db.Integer)
    active_url = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(300))
    date_created = db.Column(db.Integer)

    tags = db.relationship('Tag', backref='community_from_tags')
    community_users = db.relationship('CommunityUser', backref='community_from_community_users')

    def __init__(self, in_name, in_sponsor_id, in_type, in_private, in_active_tag_set_limit, in_gloabl_link, in_description):
        self.name = in_name
        self.name_lowercase = lower_and_remove_nonalphanumeric(in_name)
        self.sponsor_id = in_sponsor_id
        self.comm_type = in_type
        self.private = in_private
        self.active_tag_set_limit = in_active_tag_set_limit
        self.active_url = secrets.token_urlsafe(32) if (in_gloabl_link) else None
        self.desc = in_description
        self.date_created = int( time.time() )

class CommunityUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('rio_user.id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)
    admin = db.Column(db.Boolean)
    invited = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    banned = db.Column(db.Boolean)
    date_joined = db.Column(db.Integer)

    ladders = db.relationship('Ladder', backref='community_users')

    def __init__(self, in_user_id, in_comm_id, in_admin, in_invited, in_active):
        self.user_id = in_user_id
        self.community_id = in_comm_id
        self.admin = in_admin
        self.invited = in_invited
        self.active = in_active
        self.date_joined = int( time.time() )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "admin": self.admin,
            "active": self.active,
            "invited": self.invited,
            "banned": self.banned,
            "date_joined": self.date_joined,
        }

class OngoingGame(db.Model):
    game_id = db.Column(db.BigInteger, primary_key = True)
    date_time_start = db.Column(db.Integer)
    stadium_id = db.Column(db.Integer)
    away_player_id = db.Column(db.ForeignKey('rio_user.id'), nullable=False)
    home_player_id = db.Column(db.ForeignKey('rio_user.id'), nullable=False)
    tag_set_id = db.Column(db.Integer, db.ForeignKey('tag_set.id'), nullable=False)
    away_captain = db.Column(db.Integer)
    home_captain = db.Column(db.Integer)
    away_roster_0_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    away_roster_1_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    away_roster_2_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    away_roster_3_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    away_roster_4_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    away_roster_5_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    away_roster_6_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    away_roster_7_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    away_roster_8_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    home_roster_0_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    home_roster_1_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    home_roster_2_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    home_roster_3_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    home_roster_4_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    home_roster_5_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    home_roster_6_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    home_roster_7_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    home_roster_8_char = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    current_inning = db.Column(db.Integer)
    current_half_inning = db.Column(db.Integer)
    current_away_score = db.Column(db.Integer)
    current_home_score = db.Column(db.Integer)
    current_away_stars = db.Column(db.Integer)
    current_home_stars = db.Column(db.Integer)
    current_outs = db.Column(db.Integer)
    current_runner_1b = db.Column(db.Boolean)
    current_runner_2b = db.Column(db.Boolean)
    current_runner_3b = db.Column(db.Boolean)
    batter_roster_loc = db.Column(db.Integer)
    pitcher_roster_loc = db.Column(db.Integer)

    away_user = db.relationship('RioUser', foreign_keys = [away_player_id], backref = 'ongoing_away_games')
    home_user = db.relationship('RioUser', foreign_keys = [home_player_id], backref = 'ongoing_home_games')
    tag_set = db.relationship('TagSet', backref = 'ongoing_games')

    def to_dict(self):
        return {
            "away_player": self.away_user.username,
            "home_player": self.home_user.username,
            "tag_set": self.tag_set_id,
            "away_captain": self.away_captain,
            "home_captain": self.home_captain,
            "start_time": self.date_time_start,
            "stadium_id": self.stadium_id,
            "inning": self.current_inning,
            "half_inning": self.current_half_inning,
            "away_score": self.current_away_score,
            "home_score": self.current_home_score,
            "away_roster_0_char": self.away_roster_0_char,
            "away_roster_1_char": self.away_roster_1_char,
            "away_roster_2_char": self.away_roster_2_char,
            "away_roster_3_char": self.away_roster_3_char,
            "away_roster_4_char": self.away_roster_4_char,
            "away_roster_5_char": self.away_roster_5_char,
            "away_roster_6_char": self.away_roster_6_char,
            "away_roster_7_char": self.away_roster_7_char,
            "away_roster_8_char": self.away_roster_8_char,
            "home_roster_0_char": self.home_roster_0_char,
            "home_roster_1_char": self.home_roster_1_char,
            "home_roster_2_char": self.home_roster_2_char,
            "home_roster_3_char": self.home_roster_3_char,
            "home_roster_4_char": self.home_roster_4_char,
            "home_roster_5_char": self.home_roster_5_char,
            "home_roster_6_char": self.home_roster_6_char,
            "home_roster_7_char": self.home_roster_7_char,
            "home_roster_8_char": self.home_roster_8_char,
            "away_stars": self.current_away_stars,
            "home_stars": self.current_home_stars,
            "outs": self.current_outs,
            "runner_on_first": self.current_runner_1b,
            "runner_on_second": self.current_runner_2b,
            "runner_on_third": self.current_runner_3b,
            "batter": self.batter_roster_loc,
            "pitcher": self.pitcher_roster_loc
        }


class Game(db.Model):
    game_id = db.Column(db.BigInteger, primary_key = True)
    away_player_id = db.Column(db.ForeignKey('rio_user.id'), nullable=False) #One-to-One
    home_player_id = db.Column(db.ForeignKey('rio_user.id'), nullable=False) #One-to-One
    date_time_start = db.Column(db.Integer)
    date_time_end = db.Column(db.Integer)
    ranked = db.Column(db.Boolean)
    netplay = db.Column(db.Boolean)
    stadium_id = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    home_score = db.Column(db.Integer)
    innings_selected = db.Column(db.Integer)
    innings_played = db.Column(db.Integer)
    quitter = db.Column(db.Integer) #0=None, 1=Away, 2=Home
    valid = db.Column(db.Boolean)
    average_ping = db.Column(db.Integer)
    lag_spikes = db.Column(db.Integer)
    version = db.Column(db.String(50))

    character_game_summary = db.relationship('CharacterGameSummary', backref='game')
    event = db.relationship('Event', backref='game')
    game_history = db.relationship("GameHistory", backref='game')

    def to_dict(self):
        return {
            'game_id': self.game_id,
            'away_player_id': self.away_player_id,
            'home_player_id': self.home_player_id,
            'away_score': self.away_score,
            'home_score': self.home_score,
            'innings_played': self.innings_played            
        }

class CharacterGameSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.BigInteger, db.ForeignKey('game.game_id'), nullable=False)
    char_id = db.Column(db.Integer, db.ForeignKey('character.char_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('rio_user.id'), nullable=False)
    character_position_summary_id = db.Column(db.Integer, db.ForeignKey('character_position_summary.id'), nullable=False)
    team_id = db.Column(db.Integer)
    roster_loc = db.Column(db.Integer) #0-8
    captain = db.Column(db.Boolean)
    superstar = db.Column(db.Boolean)
    fielding_hand = db.Column(db.Boolean)
    batting_hand = db.Column(db.Boolean)
    #Defensive Stats
    batters_faced = db.Column(db.Integer)
    runs_allowed = db.Column(db.Integer)
    earned_runs = db.Column(db.Integer)
    batters_walked = db.Column(db.Integer)
    batters_hit = db.Column(db.Integer)
    hits_allowed = db.Column(db.Integer)
    homeruns_allowed = db.Column(db.Integer)
    pitches_thrown = db.Column(db.Integer)
    stamina = db.Column(db.Integer)
    was_pitcher = db.Column(db.Integer)
    strikeouts_pitched = db.Column(db.Integer)
    star_pitches_thrown = db.Column(db.Integer)
    big_plays = db.Column(db.Integer)
    outs_pitched = db.Column(db.Integer)
    #Offensive Stats
    at_bats = db.Column(db.Integer)
    plate_appearances = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    singles = db.Column(db.Integer)
    doubles = db.Column(db.Integer)
    triples = db.Column(db.Integer)
    homeruns = db.Column(db.Integer)
    successful_bunts = db.Column(db.Integer)
    sac_flys = db.Column(db.Integer)
    strikeouts = db.Column(db.Integer)
    walks_bb = db.Column(db.Integer)
    walks_hit = db.Column(db.Integer)
    rbi = db.Column(db.Integer)
    bases_stolen = db.Column(db.Integer)
    star_hits = db.Column(db.Integer)
    #Star tracking (Not in JSON. Calculated in populate_db)
    offensive_star_swings = db.Column(db.Integer)
    offensive_stars_used = db.Column(db.Integer)
    offensive_stars_put_in_play = db.Column(db.Integer)
    offensive_star_successes = db.Column(db.Integer)
    offensive_star_chances = db.Column(db.Integer)
    offensive_star_chances_won = db.Column(db.Integer)
    defensive_star_pitches = db.Column(db.Integer)
    defensive_stars_used = db.Column(db.Integer)
    defensive_star_successes = db.Column(db.Integer)
    defensive_star_chances = db.Column(db.Integer)
    defensive_star_chances_won = db.Column(db.Integer)

    fielding_summary = db.relationship('FieldingSummary', backref = 'fielding_summary')
    events_when_pitcher = db.relationship('Event', foreign_keys = 'Event.pitcher_id', backref='character_game_summary_of_event_pitcher')
    events_when_catcher = db.relationship('Event', foreign_keys = 'Event.catcher_id', backref='character_game_summary_of_event_catcher')
    events_when_batter = db.relationship('Event', foreign_keys = 'Event.batter_id', backref = 'character_game_summary_of_event_batter')
    runner = db.relationship('Runner', foreign_keys = 'Runner.runner_character_game_summary_id', backref = 'character_game_summary_runner')

    def to_dict(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'char_id': self.char_id,
            "user_id": self.user_id,
            "team_id": self.team_id
        }

class CharacterPositionSummary(db.Model):
    id                   = db.Column(db.Integer, primary_key=True)
    pitches_at_p         = db.Column(db.Integer)
    pitches_at_c         = db.Column(db.Integer)
    pitches_at_1b        = db.Column(db.Integer)
    pitches_at_2b        = db.Column(db.Integer)
    pitches_at_3b        = db.Column(db.Integer)
    pitches_at_ss        = db.Column(db.Integer)
    pitches_at_lf        = db.Column(db.Integer)
    pitches_at_cf        = db.Column(db.Integer)
    pitches_at_rf        = db.Column(db.Integer)
    batter_outs_at_p     = db.Column(db.Integer)
    batter_outs_at_c     = db.Column(db.Integer)
    batter_outs_at_1b    = db.Column(db.Integer)
    batter_outs_at_2b    = db.Column(db.Integer)
    batter_outs_at_3b    = db.Column(db.Integer)
    batter_outs_at_ss    = db.Column(db.Integer)
    batter_outs_at_lf    = db.Column(db.Integer)
    batter_outs_at_cf    = db.Column(db.Integer)
    batter_outs_at_rf    = db.Column(db.Integer)
    outs_at_p            = db.Column(db.Integer)
    outs_at_c            = db.Column(db.Integer)
    outs_at_1b           = db.Column(db.Integer)
    outs_at_2b           = db.Column(db.Integer)
    outs_at_3b           = db.Column(db.Integer)
    outs_at_ss           = db.Column(db.Integer)
    outs_at_lf           = db.Column(db.Integer)
    outs_at_cf           = db.Column(db.Integer)
    outs_at_rf           = db.Column(db.Integer)

    character_game_summary = db.relationship('CharacterGameSummary', backref = 'character_position_summary')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.BigInteger, db.ForeignKey('game.game_id'), nullable=False)
    pitcher_id = db.Column(db.Integer, db.ForeignKey('character_game_summary.id'), nullable=False) #Based on "Pitcher Roster Loc" in JSON
    batter_id = db.Column(db.Integer, db.ForeignKey('character_game_summary.id'), nullable=False)
    catcher_id = db.Column(db.Integer, db.ForeignKey('character_game_summary.id'), nullable=False)
    runner_on_0 = db.Column(db.Integer, db.ForeignKey('runner.id'), nullable=False)
    runner_on_1 = db.Column(db.Integer, db.ForeignKey('runner.id'), nullable=True)
    runner_on_2 = db.Column(db.Integer, db.ForeignKey('runner.id'), nullable=True)
    runner_on_3 = db.Column(db.Integer, db.ForeignKey('runner.id'), nullable=True)
    pitch_summary_id = db.Column(db.Integer, db.ForeignKey('pitch_summary.id'), nullable=True)
    event_num = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    home_score = db.Column(db.Integer)
    inning = db.Column(db.Integer)
    half_inning = db.Column(db.Integer)
    chem_links_ob = db.Column(db.Integer)
    star_chance = db.Column(db.Integer)
    away_stars = db.Column(db.Integer)
    home_stars = db.Column(db.Integer)
    pitcher_stamina = db.Column(db.Integer)
    outs = db.Column(db.Integer)
    balls = db.Column(db.Integer)
    strikes = db.Column(db.Integer)
    result_num_of_outs = db.Column(db.Integer)
    result_rbi = db.Column(db.Integer)
    result_of_ab = db.Column(db.Integer)

class PitchSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_summary_id = db.Column(db.Integer, db.ForeignKey('contact_summary.id'), nullable=True)
    pitch_type = db.Column(db.Integer)
    charge_pitch_type = db.Column(db.Integer)
    star_pitch = db.Column(db.Integer)
    pitch_speed = db.Column(db.Integer)
    d_ball = db.Column(db.Boolean)
    type_of_swing = db.Column(db.Integer)
    ball_position_strikezone = db.Column(db.Integer)
    in_strikezone = db.Column(db.Boolean)
    bat_x_contact_pos = db.Column(db.Float)
    bat_z_contact_pos = db.Column(db.Float)

    event = db.relationship('Event', backref='pitch_summary')

class ContactSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fielding_summary_id = db.Column(db.Integer, db.ForeignKey('fielding_summary.id'), nullable=True)
    type_of_contact = db.Column(db.Integer)
    charge_power_up = db.Column(db.Float)
    charge_power_down = db.Column(db.Float)
    star_swing_five_star = db.Column(db.Integer)
    input_direction = db.Column(db.Integer)
    input_direction_stick = db.Column(db.Integer)
    frame_of_swing_upon_contact = db.Column(db.Integer)
    ball_power = db.Column(db.Integer)
    ball_horiz_angle = db.Column(db.Integer)
    ball_vert_angle = db.Column(db.Integer)
    contact_absolute = db.Column(db.Float)
    contact_quality = db.Column(db.Float)
    rng1 = db.Column(db.Float)
    rng2 = db.Column(db.Float)
    rng3 = db.Column(db.Float)
    ball_x_velocity = db.Column(db.Float)
    ball_y_velocity = db.Column(db.Float)
    ball_z_velocity = db.Column(db.Float)
    ball_x_contact_pos = db.Column(db.Float)
    ball_z_contact_pos = db.Column(db.Float)
    ball_x_landing_pos = db.Column(db.Float)
    ball_y_landing_pos = db.Column(db.Float)
    ball_z_landing_pos = db.Column(db.Float)
    ball_max_height = db.Column(db.Float)
    ball_hang_time = db.Column(db.Float)
    primary_result = db.Column(db.Integer)
    secondary_result = db.Column(db.Integer)

    pitch_summary = db.relationship('PitchSummary', backref= 'contact_summary')

class FieldingSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fielder_character_game_summary_id = db.Column(db.Integer, db.ForeignKey('character_game_summary.id'), nullable=False)
    position = db.Column(db.Integer)
    action = db.Column(db.Integer)
    jump = db.Column(db.Integer)
    bobble = db.Column(db.Integer)
    swap = db.Column(db.Boolean)
    manual_select = db.Column(db.Integer)
    fielder_x_pos = db.Column(db.Float)
    fielder_y_pos = db.Column(db.Float)
    fielder_z_pos = db.Column(db.Float)

    contact_summary = db.relationship('ContactSummary', backref='fielding_summary')

class Runner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    runner_character_game_summary_id = db.Column(db.Integer, db.ForeignKey('character_game_summary.id'), nullable=False)
    initial_base = db.Column(db.Integer)
    result_base = db.Column(db.Integer)
    out_type = db.Column(db.Integer)
    out_location = db.Column(db.Integer)
    steal = db.Column(db.Integer)

    events_on_0 = db.relationship('Event', foreign_keys = 'Event.runner_on_0', backref = 'runner_0')
    events_on_1 = db.relationship('Event', foreign_keys = 'Event.runner_on_1', backref = 'runner_1')
    events_on_2 = db.relationship('Event', foreign_keys = 'Event.runner_on_2', backref = 'runner_2')
    events_on_3 = db.relationship('Event', foreign_keys = 'Event.runner_on_3', backref = 'runner_3')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=True)
    name = db.Column(db.String(32), unique=True)
    name_lowercase = db.Column(db.String(32), unique=True)
    tag_type = db.Column(db.String(16))
    desc = db.Column(db.String(300))
    active = db.Column(db.Boolean)
    date_created = db.Column(db.Integer)

    def __init__(self, in_comm_id, in_tag_name, in_tag_type, in_desc):
        self.community_id = in_comm_id
        self.name = in_tag_name
        self.name_lowercase = lower_and_remove_nonalphanumeric(in_tag_name)
        self.tag_type = in_tag_type
        self.desc = in_desc
        self.active = True
        self.date_created = int( time.time() )
    
    def to_dict(self):
        return {
            'id': self.id,
            'comm_id': self.community_id,
            'name': self.name,
            'type': self.tag_type,
            'desc': self.desc,
            'active': self.active,
            'date_created': self.date_created
        }

class GeckoCodeTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    gecko_code_desc = db.Column(db.Text)
    gecko_code = db.Column(db.Text)

    tag = db.relationship('Tag', backref='tag')

    def __init__(self, in_tag_id, in_gecko_code_desc, in_gecko_code):
        self.tag_id = in_tag_id
        self.gecko_code_desc = in_gecko_code_desc
        self.gecko_code = in_gecko_code
    
    def to_dict(self):
        return {
            'gecko_code_desc': self.gecko_code_desc,
            'gecko_code': self.gecko_code
        }

# Join table for tags and tag set
tagsettag = db.Table('tag_set_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('tagset_id', db.Integer, db.ForeignKey('tag_set.id'), primary_key=True)
)

class TagSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=True)
    name = db.Column(db.String(120), unique=True)
    name_lowercase = db.Column(db.String(120), unique=True)
    type = db.Column(db.String(120)) #Season, league, tournament.
    start_date = db.Column(db.Integer)
    end_date = db.Column(db.Integer)

    tags = db.relationship('Tag', secondary=tagsettag, backref='tagset', cascade='delete')

    ladder = db.relationship('Ladder', backref='tag_set')

    def __init__(self, in_comm_id, in_name, in_type, in_start, in_end):
        self.community_id = in_comm_id
        self.name = in_name
        self.name_lowercase = lower_and_remove_nonalphanumeric(in_name)
        self.type = in_type
        self.start_date = in_start
        self.end_date = in_end
    
    def to_dict(self, include_tags=True):
        ret_dict = {
            'id': self.id,
            'comm_id': self.community_id,
            'name': self.name,
            'type': self.type,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        if (include_tags):
            ret_dict['tags'] = self.expand_tag_list()
        return ret_dict

    def expand_tag_list(self):
        tag_list = list()
        for tag in self.tags:
            tag_list.append(tag.to_dict())
        return tag_list

class Ladder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_set_id = db.Column(db.Integer, db.ForeignKey('tag_set.id'), nullable=False)
    community_user_id = db.Column(db.Integer, db.ForeignKey('community_user.id'), nullable=False)
    started_searching = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    rd = db.Column(db.Integer)
    vol = db.Column(db.Float)

    def __init__(self, in_tag_set_id, in_comm_user_id, in_rating, in_rd, in_vol):
        self.tag_set_id = in_tag_set_id
        self.community_user_id = in_comm_user_id
        self.rating = in_rating
        self.rd = in_rd
        self.vol = in_vol
        self.start_searching = False

class GameHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.BigInteger, db.ForeignKey('game.game_id'), nullable=True)
    tag_set_id = db.Column(db.Integer, db.ForeignKey('tag_set.id'), nullable=False)
    winner_comm_user_id = db.Column(db.Integer, db.ForeignKey('community_user.id'), nullable=False)
    loser_comm_user_id = db.Column(db.Integer, db.ForeignKey('community_user.id'), nullable=False)
    winner_score = db.Column(db.Integer)
    loser_score = db.Column(db.Integer)
    winner_elo = db.Column(db.Integer, nullable=False)
    loser_elo = db.Column(db.Integer, nullable=False)
    winner_accept = db.Column(db.Boolean)
    loser_accept = db.Column(db.Boolean, nullable=True)
    admin_accept = db.Column(db.Boolean, nullable=True)
    date_created = db.Column(db.Integer, nullable=True)

    tag_set = db.relationship('TagSet', backref = 'tag_set')

    def __init__(self, in_game_id, in_tag_set_id, in_winner_comm_id, in_loser_com_id, in_winner_score, in_loser_score, in_winner_elo, in_loser_elo, in_winner_accept, in_loser_accept, in_admin_accept):
        self.game_id = in_game_id
        self.tag_set_id = in_tag_set_id
        self.winner_comm_user_id = in_winner_comm_id
        self.loser_comm_user_id = in_loser_com_id
        self.winner_score = in_winner_score
        self.loser_score = in_loser_score
        self.winner_elo = in_winner_elo
        self.loser_elo = in_loser_elo

        # Initializing a GameHistory to false is really saying this user hasn't accpeted or rejected yet. So we'll set that to NULL
        self.winner_accept = in_winner_accept if (in_winner_accept == True) else None
        self.loser_accept = in_loser_accept if (in_loser_accept == True) else None
        self.admin_accept = in_admin_accept if (in_admin_accept == True) else None
        self.date_created = int( time.time() )

class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(50), unique=True)
    date_created = db.Column(db.Integer)
    pings_daily = db.Column(db.Integer)
    pings_weekly = db.Column(db.Integer)
    last_ping_date = db.Column(db.Integer)
    total_pings = db.Column(db.Integer)

    user = db.relationship('RioUser', backref='api_key')

    def __init__(self):
        self.date_created = int(time.time())
        self.api_key = secrets.token_urlsafe(32)
        self.pings_today = 0
        self.total_pings = 0
        self.pings_daily = 0
        self.pings_weekly = 0
