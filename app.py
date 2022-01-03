import os.path
from decouple import config

import secrets #For key generation
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_login      import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_bcrypt     import Bcrypt


# ===== Setup =====
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
DB_URI = 'sqlite:///{}'.format(DB_PATH)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
 # Set up the App SECRET_KEY
app.config['SECRET_KEY'] = config('SECRET_KEY', default='S#perS3crEt_007')

db = SQLAlchemy(app)
ma = Marshmallow(app)

bc = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)

# ===== Models =====
class User(db.Model, UserMixin):
    id       = db.Column(db.Integer,     primary_key=True)
    username = db.Column(db.String(64),  unique = True)
    email    = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(500))
    rio_key  = db.Column(db.String(50), unique = True)

    def __init__(self, in_username, in_email, in_password):
        self.username = in_username
        self.email    = in_email
        self.password = bc.generate_password_hash(in_password)
        self.rio_key  = secrets.token_urlsafe(32)

class Game(db.Model):
  game_id = db.Column(db.String(255), primary_key = True)
  date_time = db.Column(db.String(255))
  ranked = db.Column(db.Integer)
  stadium_id = db.Column(db.String(255))
  # away_player_id = db.Column(db.ForeignKey('user.rio_key'), nullable=True) #One-to-One
  # home_player_id = db.Column(db.ForeignKey('user.rio_key'), nullable=True) #One-to-One
  away_score = db.Column(db.Integer)
  home_score = db.Column(db.Integer)
  innings_selected = db.Column(db.Integer)
  innings_played = db.Column(db.Integer)
  quitter = db.Column(db.Integer) #0=None, 1=Away, 2=Home

  game_character_summary = db.relationship('CharacterGameSummary', backref='game')

class CharacterGameSummary(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  game_id = db.Column(db.String(255), db.ForeignKey('game.game_id'), nullable=False)
  team_id = db.Column(db.Integer)
  roster_loc = db.Column(db.Integer) #0-8
  superstar = db.Column(db.Boolean)

  # #Defensive stats
  batters_faced = db.Column(db.Integer)
  runs_allowed = db.Column(db.Integer)
  batters_walked = db.Column(db.Integer)
  batters_hit = db.Column(db.Integer)
  hits_allowed = db.Column(db.Integer)
  homeruns_allowed = db.Column(db.Integer)
  pitches_thrown = db.Column(db.Integer)
  stamina = db.Column(db.Integer)
  was_pitcher = db.Column(db.Integer)
  batter_outs = db.Column(db.Integer)
  strike_outs_pitched = db.Column(db.Integer)
  star_pitches_thrown = db.Column(db.Integer)
  big_plays = db.Column(db.Integer)
  #Rio curated stats
  innings_pitched = db.Column(db.Integer)

  #Offensive Stats
  at_bats = db.Column(db.Integer)
  hits = db.Column(db.Integer)
  singles = db.Column(db.Integer)
  doubles = db.Column(db.Integer)
  triples = db.Column(db.Integer)
  homeruns = db.Column(db.Integer)
  strike_outs = db.Column(db.Integer)
  walks_bb = db.Column(db.Integer)
  walks_hit = db.Column(db.Integer)
  rbi = db.Column(db.Integer)
  bases_stolen = db.Column(db.Integer)
  star_hits = db.Column(db.Integer)


# ===== Schema =====

class UserSchema(ma.Schema):
  class Meta:
      fields = ('username', 'email', 'rio_key')

class GameSchema(ma.Schema):
  class Meta:
    fields = (
      'game_id',
      'date_time',
      'ranked',
      'stadium_id',
      # 'away_player_id',
      # 'home_player_id',
      'away_score',
      'home_score',
      'innings_selected',
      'innings_played',
      'quitter',
    )

class CharacterGameSummarySchema(ma.Schema):
  class Meta:
    fields = (
      'id',
      'game_id',
      'team_id',
      'roster_loc',
      'superstar',

      #Defensive stats
      'batters_faced',
      'runs_allowed',
      'batters_walked',
      'batters_hit',
      'hits_allowed',
      'homeruns_allowed',
      'pitches_thrown',
      'stamina',
      'was_pitcher',
      'batter_outs',
      'strike_outs_pitched',
      'star_pitches_thrown',
      'big_plays',
      #Rio curated stats
      'innings_pitched',

      #Offensive Stats
      'at_bats',
      'hits',
      'singles',
      'doubles',
      'triples',
      'homeruns',
      'strike_outs',
      'walks_bb',
      'walks_hit',
      'rbi',
      'bases_stolen',
      'star_hits',
    )

user_schema = UserSchema()
game_schema = GameSchema()
games_schema = GameSchema(many=True)
character_game_summary_schema = CharacterGameSummarySchema()

# ===== API Routes =====
@app.route('/')
def index():
    return 'API online...'


# == User Routes ==

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout/')
def logout():
    logout_user()
    
    resp = jsonify(success=True)
    return resp

@app.route('/register/', methods=['POST'])
def register():    
    in_username = request.json['Username']
    in_password = request.json['Password']
    in_email    = request.json['Email']

    # filter User out of database through username
    user = User.query.filter_by(username=in_username).first()

    # filter User out of database through email
    user_by_email = User.query.filter_by(email=in_email).first()

    if user or user_by_email:
        return abort(409, description='Username has already been taken')
    elif in_username.isalnum() == False:
        return abort(406, description='Provided username is not alphanumeric')
    else:
        new_user = User(in_username, in_email, in_password)
        db.session.add(new_user)
        db.session.commit()

    return user_schema.dump(new_user)

# Authenticate user, login via username or email
@app.route('/login/', methods=['POST'])
def login():
    in_username = request.json['Username']
    in_password = request.json['Password']
    in_email    = request.json['Email']

    # filter User out of database through username
    user = User.query.filter_by(username=in_username).first()

    # filter User out of database through email
    user_by_email = User.query.filter_by(email=in_email).first()

    if user or user_by_email:
        user_to_login = user if user else user_by_email
        if bc.check_password_hash(user_to_login.password, in_password):
            login_user(user_to_login)
            return user_schema.dump(user_to_login)
        else:
            return abort(401, description='Incorrect password')
    else:
        return abort(406, description='User does not exist')

#GET will retreive user key, POST with empty JSON will generate new rio key and return it
@app.route('/key/', methods=['GET', 'POST'])
@login_required
def update_rio_key():
    if current_user.is_authenticated:
        # Return Key
        if request.method == 'GET':
            return user_schema.dump(current_user)
        # Generate new key and return it
        elif request.method == 'POST':
            current_user.rio_key  = secrets.token_urlsafe(32)            
            db.session.commit()
            return user_schema.dump(current_user)
    
# == Game Routes ==

@app.route('/game/', methods=['POST'])
def populate_db():

  game = Game(
    game_id = request.json['GameID'],
    date_time = request.json['Date'],
    ranked = request.json['Ranked'],
    stadium_id = request.json['StadiumID'],
    away_score = request.json['Away Score'],
    home_score = request.json['Home Score'],
    innings_selected = request.json['Innings Selected'],
    innings_played = request.json['Innings Played'],
    quitter = request.json['Quitter Team'],
  )
  db.session.add(game)
  

  # Game Characters
  player_stats = request.json['Player Stats']
  for character in player_stats:
    defensive_stats = character['Defensive Stats']
    offensive_stats = character['Offensive Stats']

    character_game_summary = CharacterGameSummary(
      game = game,
      team_id = 0 if character['Team'] == 'Home' else 1,
      roster_loc = character['RosterID'],
      superstar = True if character['Is Starred'] == 1 else False,

      #Defensive stats
      batters_faced = defensive_stats['Batters Faced'],
      runs_allowed = defensive_stats['Runs Allowed'],
      batters_walked = defensive_stats['Batters Walked'],
      batters_hit = defensive_stats['Batters Hit'],
      hits_allowed = defensive_stats['Hits Allowed'],
      homeruns_allowed = defensive_stats['HRs Allowed'],
      pitches_thrown = defensive_stats['Pitches Thrown'],
      stamina = defensive_stats['Stamina'],
      was_pitcher = defensive_stats['Was Pitcher'],
      batter_outs = defensive_stats['Batter Outs'],
      strike_outs_pitched = defensive_stats['Strikeouts'],
      star_pitches_thrown = defensive_stats['Star Pitches Thrown'],
      big_plays = defensive_stats['Big Plays'],
      #Rio curated stats
      innings_pitched = defensive_stats['Innings Pitched'],

      #Offensive Stats
      at_bats = offensive_stats['At Bats'],
      hits = offensive_stats['Hits'],
      singles = offensive_stats['Singles'],
      doubles = offensive_stats['Doubles'],
      triples = offensive_stats['Triples'],
      homeruns = offensive_stats['Homeruns'],
      strike_outs = offensive_stats['Strikeouts'],
      walks_bb = offensive_stats['Walks (4 Balls)'],
      walks_hit = offensive_stats['Walks (Hit)'],
      rbi = offensive_stats['RBI'],
      bases_stolen = offensive_stats['Bases Stolen'],
      star_hits = offensive_stats['Star Hits'],
    )

    db.session.add(character_game_summary)


  db.session.commit()
  return game_schema.jsonify(game)

if __name__ == '__main__':
    app.run(debug=True)