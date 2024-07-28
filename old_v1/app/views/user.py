from flask import render_template, request, jsonify, abort
from flask import current_app as app
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies
import secrets
from datetime import datetime, timedelta, timezone
from .. import bc
from ..models import db, RioUser, UserGroup, UserGroupUser
from ..util import *
from app.utils.send_email import send_email
from app.views.community import add_user_to_all_comms

# === User Registration Front End ===
@app.route('/signup/')
def display_signup_page():
    return render_template('signup.html')

# === User registration endpoints ===
@app.route('/register/', methods=['POST'])
def register():
    in_username = request.json['Username']
    username_lowercase = lower_and_remove_nonalphanumeric(in_username)
    in_password = request.json['Password']
    in_email    = request.json['Email'].lower()

    user = RioUser.query.filter_by(username_lowercase=username_lowercase).first()
    user_by_email = RioUser.query.filter_by(email=in_email).first()

    if user or user_by_email:
        return abort(409, description='Username or Email has already been taken')
    elif in_username.isalnum() == False:
        return abort(406, description='Provided username is not alphanumeric')
    elif '@' not in in_email:
        return abort(406, description='Not a valid email')
    else:
        # === Create User row ===
        new_user = RioUser(in_username, in_email, in_password)
        db.session.add(new_user)
        db.session.commit()

        subject = 'Verify your Project Rio Account'
        html_content = (
            f'''
                <h1>Welcome to Rio Web, {in_username}!</h1>
                <p>Please click the following link to verify your email address and get your Rio Key.</p>
                <a href={'https://projectrio-api-1.api.projectrio.app/verify_email/' + new_user.active_url}>Verfiy Me!</a>
                <br/>
                <p>Happy Hitting!</p>
                <p>Rio Team</p>
            '''
        )
        text_content = (
            f'''
                Welcome to Rio Web, {in_username}!\n
                Please click the following link to verify your email address and get your Rio Key.\n
                https://projectrio-api-1.api.projectrio.app/verify_email/{new_user.active_url}\n
                \n
                \n
                Happy hitting!\n
                Project Rio Web Team
            '''
        )

        try:
            send_email(new_user.email, subject, html_content, text_content)
        except:
            return abort(502, 'Failed to send email')
        
    return jsonify({
        'username': new_user.username
    })

@app.route('/verify_email/<active_url>', methods=['POST','GET'])
def verify_email(active_url):
    try:
        user = RioUser.query.filter_by(active_url=active_url).first()
        user.verified = True
        user.active_url = None

        user_group = UserGroup.query.filter_by(name="General").first()
        new_user_group_user = UserGroupUser(
            user_id=user.id,
            user_group_id=user_group.id
        )
        db.session.add(new_user_group_user)
        
        subject = 'Your Rio Key'
        html_content = (
            f'''
                <h1>Welcome to Rio Web, {user.username}!</h1>
                <p>Your account has been verified!</p> 
                <br/>
                <h3>Here is your Rio Key: {user.rio_key}</h3>
                <h3>Directions</h3>
                <ol>
                    <li>From the main Rio screen click "Local Play" then "Add Player"</li>
                    <li>Enter your username and Rio Key</li>
                    <li>Have fun!</li>
                </ol>
                <p>If you already have a Local Player saved with the same name...</p>
                <ol>
                    <li>Click the Local Play tab in the client</li>
                    <li>Remove your original local player name</li>
                    <li>Click "Add Player" and enter your new username and rio key</li>
                </ol>

                <br/>
                <p>Happy hitting!</p>
                <p>Rio Team</p>
            '''
        )
        text_content = (
            f'''
                Welcome to Rio Web, {user.username}!\n
                Your account has been verified!\n
                Here is your Rio Key: {user.rio_key}\n
                Directions\n
                - From the main Rio screen click "Local Play" then "Add Player"\n
                - Enter your username and Rio Key\n
                - Have fun!\n
                If you already have a Local Player saved with the same name...\n
                - Click the Local Play tab in the client\n
                - Remove your original local player name\n
                - Click "Add Player" and enter your new username and rio key\n
                \n
                Happy hitting!\n
                Project Rio Web Team
            '''
        )

        # === Add users to Official community ===
        add_user_to_all_comms(user.id, 'Official')

        try:
            send_email(user.email, subject, html_content, text_content)
        except:
            return abort(502, 'Failed to send email')

        db.session.add(user)
        db.session.commit()
        return {
            'Rio Key': user.rio_key,
        }, 200
    except:
        return abort(422, 'Invalid url')


# === Password change endpoints ===
@app.route('/request_password_change/', methods=['POST'])
def request_password_change():
    if '@' in request.json['username or email']:
        email_lowercase = request.json['username or email'].lower()
        user = RioUser.query.filter_by(email=email_lowercase).first()
    else:
        username_lower = lower_and_remove_nonalphanumeric(request.json['username or email'])
        user = RioUser.query.filter_by(username_lowercase=username_lower).first()

    if not user:
        abort(408, 'Corresponding user does not exist')

    if user.verified == False:
        abort(401, 'Email unverified')

    active_url = secrets.token_urlsafe(32)
    user.active_url = active_url
    db.session.add(user)
    db.session.commit()

    subject = 'Project Rio Password Reset Request'
    html_content =  (
        f'''
            Dear {user.email},\n
            \n
            We received a password reset request for your account. If you did not make this request, please ignore this email.\n
            Otherwise, follow this link to reset your password:\n
            <a href={cURL + '/login/reset_password/' + user.active_url}>Reset Password</a>\n
            \n
            Happy hitting!\n
            Project Rio Web Team     
        '''
    )
    text_content = (
        f'''
            Dear {user.email},\n
            We received a password reset request for your account. If you did not make this request, please ignore this email.\n
            Otherwise, follow this link to reset your password:\n
            {cURL}/login/reset_password/{user.active_url}\n
            \n
            Happy hitting!\n
            Project Rio Web Team     

        '''
    )
    
    try:
        send_email(user.email, subject, html_content, text_content)
    except:
        abort(502, 'Failed to send email')

    return {
        'msg': 'Link emailed...'
    }


@app.route('/change_password/', methods=['POST'])
def change_password():
    active_url = request.json['active_url']
    password = request.json['password']

    user = RioUser.query.filter_by(active_url=active_url).first()

    if not user:
        return abort(422, 'Invalid Key')

    if user.verified == False:
        return abort(401, 'Email unverified')

    user.password = bc.generate_password_hash(password)
    user.active_url = None
    db.session.add(user)
    db.session.commit()

    return {
        'msg': 'Password changed...'
    }, 200



# === JWT endpoints ===
@app.route('/login/', methods=['POST'])
def login():
    in_username = lower_and_remove_nonalphanumeric(request.json['Username'])
    in_password = request.json['Password']
    in_email    = request.json['Email'].lower()

    # filter User out of database through username
    user = RioUser.query.filter_by(username_lowercase=in_username).first()

    # filter User out of database through email
    user_by_email = RioUser.query.filter_by(email=in_email).first()

    if user == user_by_email:
        if bc.check_password_hash(user.password, in_password):            
            # Creating JWT and Cookies
            response = jsonify({
                'msg': 'login successful',
                'username': user.username,
            })
            access_token = create_access_token(identity=user.username)
            set_access_cookies(response, access_token)

            return response
        else:
            return abort(401, description='Incorrect password')
    else:
        return abort(408, description='Incorrect Username or Password')

@app.route('/logout/', methods=['POST'])
def logout():    
    response = jsonify({'msg': 'logout successful'})
    unset_jwt_cookies(response)
    return response

@app.route('/validate_JWT/', methods = ['GET'])
@jwt_required(optional=True)
def validate_JWT():
    try:
        current_user_username = get_jwt_identity()
        return jsonify(logged_in_as=current_user_username)
    except:
        return 'No JWT...'

# Refresh any JWT within 7 days of expiration after requests
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()['exp']
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(days=7))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where JWT is invalid, return original response
        return response



# === Get/Set user settings ===
#Generates a new Rio Key and sends it in an email.
@app.route('/request_new_rio_key/', methods=['GET'])
def update_rio_key():    
    email_lowercase = request.args.get("email").lower()
    user = RioUser.query.filter_by(email=email_lowercase).first()

    if not user:
        return "Invalid email provided."

    user.rio_key = secrets.token_urlsafe(32)
    db.session.commit()

    subject = 'Your New Rio Key'
    html_content = (
        f'''
            <h1>Hey, {user.username}!</h1>
            <p>Here's the new rio key you requested:</p>
            <p>{user.rio_key}</p>
            <br/>
            <p>Happy Hitting!</p>
            <p>Rio Team</p>
        '''
    )
    text_content = (
        f'''
            Hey, {user.username}!\n
            Here's the new rio key you requested:\n
            {user.rio_key}\n
            \n
            \n
            Happy hitting!\n
            Rio Team
        '''
    )

    try:
        send_email(user.email, subject, html_content, text_content)
    except:
        abort(502, 'Failed to send email')

    return "Your new rio key has been sent to your email address!"

#GET retreives user privacy, POST with empty JSON will swap privacy setting and return it
@app.route('/set_privacy/', methods = ['GET', 'POST'])
@jwt_required()
def set_privacy():
    current_user_username = get_jwt_identity()
    current_user = RioUser.query.filter_by(username=current_user_username).first()

    if request.method == 'GET':
        return jsonify({
            'private': current_user.private
        })
    if request.method == 'POST':
        current_user.private = not current_user.private
        db.session.commit()
        return jsonify({
            'private': current_user.private
        })


'''
@ Description: Returns tags available to a user
@ Params:
    - username: username to get available tags for. 
@ Output:
    - List of available tags
@ Example URL: http://127.0.0.1:5000/user/tags/?username=GenericHomeUser&username=GenericAwayUser
'''
@app.route('/user/tags/', methods = ['GET'])
def get_users_tags():
    if (app.config['rio_env'] == "production"):
        return abort(404, description='Endpoint not ready for production')
    
    in_username_lowercase = request.args.get("username")
    user = RioUser.query.filter_by(username_lowercase=in_username_lowercase).first()

    if not user:
        return abort(422, 'Invalid Username')

    game_tags_query = (
        'SELECT \n'
        'tag.name \n'
        'FROM tag \n'
        'LEFT JOIN game_tag ON tag.id = game_tag.tag_id \n'
        'LEFT JOIN game ON game_tag.game_id = game.game_id \n'
        'WHERE \n'
        f'game.away_player_id = {user.id} OR game.home_player_id = {user.id} \n'
        'GROUP BY \n'
        'tag.name \n'
    )

    community_tags_query = (
        'SELECT \n '
        'tag.name \n '
        'FROM tag \n'
        'LEFT JOIN community ON tag.community_id = community.id \n'
        'LEFT JOIN community_user ON community.id = community_user.community_id \n'
        f'WHERE community_user.user_id = {user.id} \n'
        'GROUP BY \n'
        'tag.name \n'
    )

    game_tags = db.session.execute(game_tags_query).all()
    community_tags = db.session.execute(community_tags_query).all()

    tags = list()

    for tag in game_tags:
        tags.append(tag.name)

    for tag in community_tags:
        if tag.name not in tags:
            tags.append(tag.name)

    return {
        "available_tags": tags
    }, 200


'''
@ Description: Returns list of communities a user is a member of
@ Params:
    - username: username to get communities for. 
@ Output:
    - List of communities
@ Example URL: http://127.0.0.1:5000/user/communities/?username=GenericHomeUser&username=GenericAwayUser
'''

@app.route('/user/communities/', methods = ['GET'])
def get_users_communities():
    if (app.config['rio_env'] == "production"):
        return abort(404, description='Endpoint not ready for production')

    in_username_lowercase = lower_and_remove_nonalphanumeric(request.json['username'])
    user = RioUser.query.filter_by(username_lowercase=in_username_lowercase).first()

    if not user:
        return abort(422, 'Invalid Username')

    communities_query = (
        'SELECT \n '
        'community.name \n '
        'FROM community \n'
        'LEFT JOIN community_user ON community.id = community_user.community_id \n'
        f'WHERE community_user.user_id = {user.id} \n'
        'GROUP BY \n'
        'tag.name \n'
    )
    
    result = db.session.execute(communities_query)

    communities = list()
    for community in result:
        communities.append(community.name)

    return {
        "communities": communities
    }, 200
