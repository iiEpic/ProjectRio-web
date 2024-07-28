from flask import request, jsonify, abort
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies
from app.utils.send_email import send_email
from ..models import db, RioUser, CommunityUser, Community, Tag, TagSet
from ..consts import *
from ..util import *
from app.views.user_groups import *
import time

@app.route('/community/create', methods=['POST'])
@jwt_required(optional=True)
def community_create():
    in_comm_name = request.json['Community Name']
    in_comm_type = request.json['Type']
    private = (request.json['Private'] == 1)
    create_global_link = (request.json['Global Link'] == 1) or not private
    in_comm_desc = request.json['Description']
    
    # Get user making the new community
    #Get user via JWT or RioKey 
    user=None
    current_user_username = get_jwt_identity()
    if current_user_username:
        user = RioUser.query.filter_by(username=current_user_username).first()
    else:
        try:
            user = RioUser.query.filter_by(rio_key=request.json['Rio Key']).first()       
        except:
            return abort(409, description="No Rio Key or JWT Provided")


    comm = Community.query.filter_by(name_lowercase=lower_and_remove_nonalphanumeric(in_comm_name)).first()
    if comm != None:
        return abort(409, description='Community name already in use')
    if user == None:
        return abort(409, description='Username associated with JWT not found. Community not created')
    if in_comm_name.isalnum() == False:
        return abort(406, description='Provided community name is not alphanumeric. Community not created')
    if in_comm_type not in cCOMM_TYPES.values():
        return abort(410, description='Invalid community type')
    if in_comm_type == 'Official' and not is_user_in_groups(user.id, ['Admin']):
        return abort(411, description='Non admin user cannot create official community')
    if not is_user_in_groups(user.id, cPATREON_TIERS) and not is_user_in_groups(user.id, ['Admin']):
        return abort(412, description='Creator is not a patron')

    #Make sure that community does not use the same name as a tag
    tag = Tag.query.filter_by(name_lowercase=lower_and_remove_nonalphanumeric(in_comm_name)).first()
    tagset = TagSet.query.filter_by(name_lowercase=lower_and_remove_nonalphanumeric(in_comm_name)).first()

    if tag != None or tagset != None:
        return abort(413, description='Name already in use (Tag or TagSet)')

    # Check that patron can sponsor a new community
    communities_sponsored = Community.query.filter(Community.sponsor_id==user.id).count()

    limit_query = (
        'SELECT \n'
        'rio_user.id, \n'
        'MAX(user_group.sponsor_limit) AS sponsor_limit \n'
        'FROM rio_user \n'
        'JOIN user_group_user ON rio_user.id = user_group_user.user_id \n'
        'JOIN user_group ON user_group_user.user_group_id = user_group.id \n'
        f'WHERE rio_user.id = {user.id} \n'
        'GROUP BY rio_user.id \n'
    )
    results = db.session.execute(limit_query).first()
    sponsor_limit = 0 if results == None else results._asdict()['sponsor_limit']

    # Results will be None if patron is not sponsoring any communities
    # Allow this community to be created if None or if under the limit
    if communities_sponsored >= sponsor_limit:
        return abort(413, description='Patron has reached limit of sponsored communities')

    # === Create Community row ===
    new_comm = Community(in_comm_name, user.id, in_comm_type, private, 
                            cACTIVE_TAGSET_LIMIT, create_global_link,
                            in_comm_desc)
    db.session.add(new_comm)
    db.session.commit()

    # === Create CommunityUser (admin)
    new_comm_user = CommunityUser(user.id, new_comm.id, True, False, True)
    db.session.add(new_comm_user)
    db.session.commit()

    # === Create Community Tag ===
    new_comm_tag = Tag(new_comm.id, new_comm.name, "Community", f"Community tag for {new_comm.name}")
    db.session.add(new_comm_tag)
    db.session.commit()

    # === Send Email ===
    subject = 'ProjectRio - New community created!'
    community_type = 'private' if private else 'public'
    html_content = (
        f'''
            <h1>Congratulations on starting a new {community_type} community, {new_comm.name}!</h1>
            <br/>
            <p>Happy Hitting!</p>
            <p>Rio Team</p>
        '''
    )
    text_content = (
        f'''
            Congratulations on starting a new {community_type} community, {new_comm.name}!\n
            \n
            Happy hitting!
            Project Rio Web Team
        '''
    )

    # === Take action based comm type === 
    # Add all users to new official community TODO
    if (new_comm.comm_type == 'Official'):
        add_all_users_to_comm(new_comm.id)
    try:
        send_email(user.email, subject, html_content, text_content)
    except:
        return abort(502, description='Failed to send email')

    return jsonify({
        'community name': new_comm.name,
        'private': new_comm.private,
        'active_url': new_comm.active_url
    })

@app.route('/community/join/<comm_name>', methods=['POST'])
def community_join_url_simple(comm_name):
    return community_join(comm_name, None)

@app.route('/community/join/<comm_name>/<active_url>', methods=['POST'])
def community_join_url(comm_name, active_url):
    return community_join(comm_name, active_url)

@app.route('/community/join', methods=['POST'])
@jwt_required(optional=True)
def community_join(in_comm_name = None, in_active_url = None):
    # Ways to join a community
    # If public: provide the community id
    # If private:
    #    If Global URL: provide active url
    #    If User has been invite, provide users active URL

    if in_comm_name == None:
        in_comm_name = request.json['Community Name']
    comm_name_lower = lower_and_remove_nonalphanumeric(in_comm_name)
    comm = Community.query.filter_by(name_lowercase=comm_name_lower).first()

    #Get user via JWT or RioKey 
    user=None
    current_user_username = get_jwt_identity()
    if current_user_username:
        user = RioUser.query.filter_by(username=current_user_username).first()
    else:
        try:
            user = RioUser.query.filter_by(rio_key=request.json['Rio Key']).first()       
        except:
            return abort(409, description="No Rio Key or JWT Provided")

    if user == None:
        return abort(409, description='Username associated with JWT not found.')
    if comm == None:
        return abort(409, description='Could not find community with name={in_comm_name}')

    # If community is public -> User can join
    # If community is private, has a global url, and the correct url has been provided:
        # If User already requested access or was invited -> user will be updated to member
        # If User has not previously requested access or been invited -> user will be created
    # If the community is private and the user was invited and the correct url for that user is provided -> user can join
    # If the community is private and the user was invited and the incorrect url for that user is provided -> user cannot join
    # If the community is private and the user was NOT invited -> user will request to join from admin if first time requesting


    comm_user = CommunityUser.query.filter_by(user_id=user.id, community_id=comm.id).first()

    if comm_user != None:
        if comm_user.active == True:
            return abort (410, "User already a community member")
        if comm_user.invited == True:
            comm_user.active = True
            comm_user.date_joined = int( time.time() )
            db.session.add(comm_user)
            db.session.commit()
            return jsonify({
                'community name': comm.name,
                'active': comm_user.active
            })
        if comm_user.banned == True:
            return abort (409, "User has been banned")

    #Public community
    if comm.private == False:
        if comm_user != None:
            comm_user.active = True
            comm_user.date_joined = int( time.time() )
        else:
            comm_user = CommunityUser(in_user_id=user.id, in_comm_id=comm.id, in_admin=False, in_invited=False, in_active=True)
        db.session.add(comm_user)
        db.session.commit()
        return jsonify({
            'community name': comm.name,
            'active': comm_user.active
        })
    else:
        #See if active URL has been provided in the JSON
        if in_active_url == None:
            try:
                in_active_url = request.json['URL']
            except:
                pass
        # If the community has a global link, check if user has provided that url
        if comm.active_url != None and in_active_url == comm.active_url:
            if comm_user == None: # User is joining with global link directly
                comm_user = CommunityUser(in_user_id=user.id, in_comm_id=comm.id, in_admin=False, in_invited=False, in_active=True)
            else: # User was invited or already requested access and has used the global link
                #Update user to be an active memeber
                comm_user.active = True
                comm_user.date_joined = int( time.time() )
            db.session.add(comm_user)
            db.session.commit()
            return jsonify({
                'community name': comm.name,
                'active': comm_user.active
            })
        else: # Request to join
            comm_user = CommunityUser(in_user_id=user.id, in_comm_id=comm.id, in_admin=False, in_invited=False, in_active=False)
            db.session.add(comm_user)
            db.session.commit()
            return jsonify({
                'community name': comm.name,
                'active': comm_user.active
            })

@app.route('/community/invite', methods=['POST'])
@jwt_required(optional=True)
def community_invite():

    in_comm_name = request.json['Community Name']
    comm_name_lower = lower_and_remove_nonalphanumeric(in_comm_name)
    comm = Community.query.filter_by(name_lowercase=comm_name_lower).first()

    #Get user via JWT or RioKey
    user=None
    current_user_username = get_jwt_identity()
    if current_user_username:
        user = RioUser.query.filter_by(username=current_user_username).first()
    else:
        try:
            user = RioUser.query.filter_by(rio_key=request.json['Rio Key']).first()       
        except:
            return abort(409, description="No Rio Key or JWT Provided")

    if user == None:
        return abort(409, description='Username associated with JWT not found.')
    if comm == None:
        return abort(409, description='Could not find community with name={in_comm_name}')

    #Check if CommunityUser already exists
    comm_user = CommunityUser.query.filter_by(user_id=user.id, community_id=comm.id).first()

    # If User does not exist or is not an admin of the private community they cannot invite
    if comm_user == None:
        return abort(409, description='User is not part of this community')
    if (comm.private and comm_user.admin == False):
        return abort(409, description='User is not an admin of this private community.')

    list_of_users_to_invite = request.json['Invite List']

    #Check that all users exist before sending invites
    for username in list_of_users_to_invite:
        invited_user = RioUser.query.filter_by(username_lowercase=lower_and_remove_nonalphanumeric(username)).first()
        if invited_user == None:
            return abort(409, description='User does not exist. Username={user}')

    #Entire list has been validated, add users to table and send emails
    for user in list_of_users_to_invite:
        invited_user = RioUser.query.filter_by(username_lowercase=lower_and_remove_nonalphanumeric(user)).first()

        #Now see if user has already been invited, if so skip inviting a second time.
        comm_user = CommunityUser.query.filter_by(user_id=invited_user.id, community_id=comm.id).first()

        if comm_user != None:
            if comm_user.invited == False: #User has requested to join, upgrade user to member
                comm_user.active = True
                comm_user.date_joined = int( time.time() )
                comm_user.banned = False #Lift ban if invited back
                db.session.add(comm_user)
                db.session.commit()
                # Still can continue
            #Already invited, skip inviting again
            continue
        new_comm_user = CommunityUser(in_user_id=invited_user.id, in_comm_id=comm.id, in_admin=False, in_invited=True, in_active=False)
        db.session.add(new_comm_user)
        db.session.commit()

        # === Send Email ===
        subject = 'ProjectRio - You have been invited to a community!'
        html_content = (
            f'''
                <h1>Congratulations {invited_user.username}! You have been invited to join {comm.name}!</h1>
                <p>Click the following link to join: </p>
                <a href={'https://www.projectrio-api-1.api.projectrio.app/community/join/' + comm.name + '/'}>Click here to join!</a>
                <br/>
                <p>Happy Hitting!</p>
                <p>Rio Team</p>
            '''
        )
        text_content = (
            f'''
                Congratulations {invited_user.username}! You have been invited to join {comm.name}!
                Click the following link to join:\n
                https://www.projectrio-api-1.api.projectrio.app/community/join/{comm.name}/
                \n
                \n
                Happy Hitting!\n
                Project Rio Web Team
            '''
        )

        try:
            send_email(invited_user.email, subject, html_content, text_content)
        except:
            return abort(502, description='Failed to send email')

    #Return list of usernames
    return {
            'Invited Users': list_of_users_to_invite,
        }, 200


#TODO return usernames rather than user ids
@app.route('/community/members', methods=['GET'])
@jwt_required(optional=True)
def community_members():
    in_comm_name = request.json['Community Name']
    comm_name_lower = lower_and_remove_nonalphanumeric(in_comm_name)
    comm = Community.query.filter_by(name_lowercase=comm_name_lower).first()

    #Get user via JWT or RioKey 
    user=None
    current_user_username = get_jwt_identity()
    if current_user_username:
        user = RioUser.query.filter_by(username=current_user_username).first()
    else:
        try:
            user = RioUser.query.filter_by(rio_key=request.json['Rio Key']).first()       
        except:
            return abort(409, description="No Rio Key or JWT Provided")

    if comm == None:
        return abort(409, description='Could not find community with name={in_comm_name}')
    
    if comm.private:
        if user == None:
            return abort(409, description='Must be logged in to see private community members.')
        #If user is logged in, must be a part of private community to see memebers
        else:
            comm_user = CommunityUser.query.filter_by(user_id=user.id, community_id=comm.id).first()
            if comm_user == None and comm.sponsor_id != user.id :
                return abort(409, description='Must be a member of private community to see all members.')

    #If we get to this point the user is allowed to get the memeber list
    member_list = CommunityUser.query.filter_by(community_id=comm.id)

    member_list_dicts = list()
    for member in member_list:
        #TODO figure out username rather than return the user id
        member_list_dicts.append(member.to_dict())

    return jsonify({'Members': member_list_dicts})

#TODO return usernames rather than user ids
@app.route('/community/tags', methods=['GET'])
@jwt_required(optional=True)
def community_tags():
    in_comm_name = request.json['Community Name']
    comm_name_lower = lower_and_remove_nonalphanumeric(in_comm_name)
    comm = Community.query.filter_by(name_lowercase=comm_name_lower).first()

    #Get user via JWT or RioKey
    user=None
    current_user_username = get_jwt_identity()
    if current_user_username:
        user = RioUser.query.filter_by(username=current_user_username).first()
    else:
        try:
            user = RioUser.query.filter_by(rio_key=request.json['Rio Key']).first()       
        except:
            return abort(409, description="No Rio Key or JWT Provided")
        
    if comm == None:
        return abort(409, description='Could not find community with name={in_comm_name}')
    
    if comm.private:
        if user == None:
            return abort(409, description='Must be logged in to see private community members.')
        else:
            #If user is logged in, must be a part of private community to see memebers
            comm_user = CommunityUser.query.filter_by(user_id=user.id, community_id=comm.id).first()
            if comm_user == None:
                return abort(409, description='Must be a member of private community to see all members.')

    #If we get to this point the user is allowed to get the tag list
    tag_list = Tag.query.filter_by(community_id=comm.id)

    tag_info_list = list()
    for tag in tag_list:
        tag_info_list.append(tag.to_dict())

    return jsonify({'Tags': tag_info_list})

#JSON format
'''
{
    Community Name: "NAME",
    User List: [
        {
            "Username": "USERNAME",
            "Admin": "y/n"
            "Remove": "y/n"
            "Uninvite": "y/n"
        }
    ]
    '''
@app.route('/community/manage', methods=['POST'])
@jwt_required(optional=True)
def community_manage():
    in_comm_name = request.json['Community Name']
    comm_name_lower = lower_and_remove_nonalphanumeric(in_comm_name)
    comm = Community.query.filter_by(name_lowercase=comm_name_lower).first()

    #Get user via JWT or RioKey 
    user=None
    current_user_username = get_jwt_identity()
    if current_user_username:
        user = RioUser.query.filter_by(username=current_user_username).first()
    else:
        try:
            user = RioUser.query.filter_by(rio_key=request.json['Rio Key']).first()       
        except:
            return abort(409, description="No Rio Key or JWT Provided")

    if comm == None:
        return abort(409, description='Could not find community with name={in_comm_name}')
    if user == None:
        return abort(409, description='No user logged in or associated with RioKey.')

    comm_user = CommunityUser.query.filter_by(user_id=user.id, community_id=comm.id).first()
    if (comm_user == None or comm_user.admin == False):
        return abort(409, description='User is not part of this community or not an admin.')

    list_of_users_to_manage = request.json['User List']
    #Check that all users exist before sending invites
    for user in list_of_users_to_manage:
        invited_user = RioUser.query.filter_by(username_lowercase=lower_and_remove_nonalphanumeric(user['Username'])).first()
        if invited_user == None:
            return abort(409, description=f"User does not exist. Username={user['Username']}")
        comm_user = CommunityUser.query.filter_by(user_id=invited_user.id, community_id=comm.id).first()
        if comm_user == None:
            return abort(409, description='User not a part of the community, cannot be made admin. Username={user}')

    #Entire list has been validated, add users to table and send emails
    updated_comm_users_list = list()
    for user_actions in list_of_users_to_manage:
        user = RioUser.query.filter_by(username_lowercase=lower_and_remove_nonalphanumeric(user_actions['Username'])).first()

        #Get user to update
        comm_user_to_update = CommunityUser.query.filter_by(user_id=user.id, community_id=comm.id).first()
        #Remove if specified
        try:
            if (user_actions['Remove'].lower() in ['yes', 'y', 'true', 't'] and not comm_user_to_update.admin):
                comm_user_to_update.active = False
                comm_user_to_update.invited = False
                db.session.add(comm_user_to_update)
                db.session.commit()
                updated_comm_users_list.append(comm_user_to_update.to_dict())
                continue
        except:
            pass

        #Ban
        try:
            if (user_actions['Ban'].lower() in ['yes', 'y', 'true', 't'] and not comm_user_to_update.admin):
                comm_user_to_update.active = False
                comm_user_to_update.invited = False
                comm_user_to_update.banned = True
                db.session.add(comm_user_to_update)
                db.session.commit()
                updated_comm_users_list.append(comm_user_to_update.to_dict())
                continue
        except:
            pass

        #Update admin if specified
        try:
            if (user_actions['Admin'].lower() in ['yes', 'y', 'true', 't'] and comm_user_to_update.active == True):
                comm_user_to_update.admin = True
            elif (user_actions['Admin'].lower() in ['no', 'n', 'f', 'false']):
                comm_user_to_update.admin = False
            db.session.add(comm_user_to_update)
            db.session.commit()
            updated_comm_users_list.append(comm_user_to_update.to_dict())
        except:
            pass

    return jsonify({"Members": updated_comm_users_list})

@app.route('/community/sponsor', methods=['POST'])
@jwt_required(optional=True)
def community_sponsor():
    in_comm_name = request.json['Community Name']
    comm_name_lower = lower_and_remove_nonalphanumeric(in_comm_name)
    comm = Community.query.filter_by(name_lowercase=comm_name_lower).first()


    if comm == None:
        return abort(409, description='Could not find community with name={in_comm_name}')

    # Action - Get, Remove, Add
    action = request.json['Action']
    #Get
    if action == 'Get':
        if comm.sponsor_id == None:
            return jsonify({'Sponsor': None})
        else:
            sponsor_user = RioUser.query.filter_by(id=comm.sponsor_id).first()
            return jsonify({'Sponsor': sponsor_user})

    #Get user via JWT or RioKey 
    user=None
    current_user_username = get_jwt_identity()
    if current_user_username:
        user = RioUser.query.filter_by(username=current_user_username).first()
    else:
        try:
            user = RioUser.query.filter_by(rio_key=request.json['Rio Key']).first()       
        except:
            return abort(409, description="No Rio Key or JWT Provided")

    if user == None:
        return abort(409, description='No user logged in or associated with RioKey.')

    #Remove
    if action == 'Remove':
        if comm.sponsor_id == None:
            return jsonify({'Sponsor': None})
        else:
            sponsor_user = RioUser.query.filter_by(id=comm.sponsor_id).first()
            if sponsor_user == user:
                comm.sponsor_id = None
                db.session.add(comm)
                db.session.commit()
                return jsonify({'Sponsor': None})
            else:
                return abort(409, description="Only current sponsor can withdraw sponsorship")
    #Add
    elif action == 'Add':
        if comm.sponsor_id == None:
            # Make sure that user is under limit
            communities_sponsored = Community.query.filter(Community.sponsor_id==user.id).count()

            limit_query = (
                'SELECT \n'
                'rio_user.id, \n'
                'MAX(user_group.sponsor_limit) AS sponsor_limit \n'
                'FROM rio_user \n'
                'JOIN user_group_user ON rio_user.id = user_group_user.user_id \n'
                'JOIN user_group ON user_group_user.user_group_id = user_group.id \n'
               f'WHERE rio_user.id = {user.id} \n'
                'GROUP BY rio_user.id \n'
            )
            results = db.session.execute(limit_query).first()
            sponsor_limit = 0 if results == None else results._asdict()['sponsor_limit']

            # Results will be None if patron is not sponsoring any communities
            # Allow this community to be created if None or if under the limit
            if communities_sponsored >= sponsor_limit:
                return abort(413, description='Patron has reached limit of sponsored communities')
            # Add new sponsor
            comm.sponsor_id = user.id
            db.session.add(comm)
            db.session.commit()
            return jsonify({'Sponsor': None})
        else:
            return abort(409, description="Community is already sponsored")

    return

def add_all_users_to_comm(comm_id):
    # Do not create duplicate users 
    community_user_list = CommunityUser.query.filter_by(community_id=comm_id)
    # List of all RioUser ids who are already in the comm
    existing_comm_user_rio_user_id_list = [ comm_user.user_id for comm_user in community_user_list]    

    rio_user_list = RioUser.query.all()
    for rio_user in rio_user_list:
        # Skip CommUser creation if RioUser already associated with CommUser
        if rio_user.id in existing_comm_user_rio_user_id_list:
            continue
        new_comm_user = CommunityUser(rio_user.id, comm_id, False, False, True)
        db.session.add(new_comm_user)
        db.session.commit()
    return

def add_user_to_comm(comm_id, rio_user_id):
    new_comm_user = CommunityUser(rio_user_id, comm_id, False, False, True)
    db.session.add(new_comm_user)
    db.session.commit()
    return

def add_user_to_all_comms(user_id, comm_type):
    comm_list = Community.query.filter_by(comm_type=comm_type)
    for comm in comm_list:
        new_comm_user = CommunityUser(user_id, comm.id, False, False, True)
        db.session.add(new_comm_user)
        db.session.commit()
    return
