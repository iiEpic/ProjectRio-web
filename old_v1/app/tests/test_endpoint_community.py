import json
import requests
from helpers import *
from connection import Connection
from pprint import pprint

db = Connection()

def test_community_create_official():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    #assert sponsor.add_to_group('patron: mvp') == True

    nonmember = User()
    nonmember.register()

    #Check that the new user is registered after creating a new official community

    # Assert community is not created, sponsor not admin
    community = Community(sponsor, True, False, False)
    assert community.success == False

    sponsor.verify_user()
    assert sponsor.add_to_group('admin') == True

    # Assert community IS created, sponsor is admin
    community = Community(sponsor, True, False, False)
    assert community.success == True

    # Did both users get added to the community (plus default members)
    assert len(community.members) == 3

   
def test_community_create_unofficial():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    nonmember = User()
    nonmember.register()

    #Check that the new user is registered after creating a new unofficial community

    # Assert community is not created, sponsor not admin
    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True

    # Did both users get added to the community
    assert len(community.members) == 1

    # Join community as nonmember
    assert community.join_via_request(nonmember) == True

    assert len(community.members) == 2

    assert community.get_member(nonmember).active == True

    # Extra Credit: check that a user can be invited to public community
    invitee = User()
    invitee.register()
    community.invite(sponsor, {invitee.pk: invitee})
    print('Test', community.get_member(invitee).to_dict())
    assert community.get_member(invitee).active  == False

def test_community_create_private_nolink():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    nonmember = User()
    nonmember.register()

    #Check that the new user is registered after creating a new official community

    # Assert community is not created, sponsor not admin
    community = Community(sponsor, official=False, private=True, link=False)
    assert community.success == True

    # Join community via link (should not work, user will request)
    community.join_via_url(nonmember)
    assert community.get_member(nonmember).active == False

    # Invite -> Request = Join
    invitee = User()
    invitee.register()
    community.invite(sponsor, {invitee.pk: invitee})
    assert community.get_member(invitee).active == False

    assert community.join_via_request(invitee) == True
    assert community.get_member(invitee).active == True


    # Request -> Invite = Join
    requester = User()
    requester.register()

    assert community.join_via_request(requester) == True
    assert community.get_member(requester).active == False

    community.invite(sponsor, {requester.pk: requester})
    assert community.get_member(requester).active == True

def test_community_create_private_link():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    nonmember = User()
    nonmember.register()

    #Check that the new user is registered after creating a new official community

    # Assert community is not created, sponsor not admin
    community = Community(sponsor, official=False, private=True, link=False)
    assert community.success == True

    # Join community via link (should not work, user will request)
    community.join_via_url(nonmember)
    assert community.get_member(nonmember).active == False

    # Invite -> Request = Join
    invitee = User()
    invitee.register()
    community.invite(sponsor, {invitee.pk: invitee})
    assert community.get_member(invitee).active == False

    assert community.join_via_request(invitee) == True
    assert community.get_member(invitee).active == True


    # Request -> Invite = Join
    requester = User()
    requester.register()

    assert community.join_via_request(requester) == True
    assert community.get_member(requester).active == False

    community.invite(sponsor, {requester.pk: requester})
    assert community.get_member(requester).active == True


    # Invite -> Request via = Join
    invitee = User()
    invitee.register()
    community.invite(sponsor, {invitee.pk: invitee})
    assert community.get_member(invitee).active == False

    assert community.join_via_url(invitee) == True
    assert community.get_member(invitee).active == True

def test_community_manage_admin():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    member = User()
    member.register()

    future_admin = User()
    future_admin.register()
    
    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True

    # Member join
    assert community.join_via_request(member)
    assert community.join_via_request(future_admin)

    # Upgrade future admin user as non-admin (not permitted)
    assert not community.manage(member, [future_admin], "admin")
    assert not community.get_member(future_admin).admin

    # Upgrade future admin user as admin
    assert community.manage(sponsor, [future_admin], "admin")
    assert community.get_member(future_admin).admin

def test_community_manage_ban():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    member = User()
    member.register()

    future_bannee = User()
    future_bannee.register()
    
    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True

    # Member join
    assert community.join_via_request(member)
    assert community.join_via_request(future_bannee)

    # Upgrade future admin user as non-admin (not permitted)
    assert not community.manage(member, [future_bannee], "ban")
    assert not community.get_member(future_bannee).banned

    # Upgrade future admin user as admin
    assert community.manage(sponsor, [future_bannee], "ban")
    assert community.get_member(future_bannee).banned


def test_community_manage_remove():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    member = User()
    member.register()

    future_removee = User()
    future_removee.register()
    
    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True

    # Member join
    assert community.join_via_request(member)
    assert community.join_via_request(future_removee)

    # Remove user as non-admin (not permitted)
    assert not community.manage(member, [future_removee], "remove")
    assert community.get_member(future_removee).active

    # Remove user as admin
    assert community.manage(sponsor, [future_removee], "remove")
    assert not community.get_member(future_removee).active

def test_community_tags():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    member = User()
    member.register()
    
    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True
    # Member join
    assert community.join_via_request(member)

    # Should just have community tag
    assert len(community.tags) == 1

    # Add tag with non-admin (should not work)
    tag = Tag(community.get_member(member), community)
    tag.create()
    assert not tag.success
    assert len(community.tags) == 1

    # Add tag with admin
    tag = Tag(community.founder, community)
    tag.create()

    assert tag.active
    assert tag.type == 'Component'
    assert len(community.tags) == 2

def test_community_tagsets():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True

    # Add tag with admin
    tag = Tag(community.founder, community)
    tag.create()

    tagset = TagSet(community.founder, community, [tag], 'League')
    tagset.create()

    assert tagset.success
    assert len(community.tags) == 3

def test_community_tagsets_limit():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True

    # Add tag with admin
    tag = Tag(community.founder, community)
    tag.create()

    tagsetA = TagSet(community.founder, community, [tag], 'League')
    tagsetA.create()
    tagsetB = TagSet(community.founder, community, [tag], 'League')
    tagsetB.create()
    tagsetC = TagSet(community.founder, community, [tag], 'League')
    tagsetC.create()
    tagsetD = TagSet(community.founder, community, [tag], 'League')
    tagsetD.create()
    tagsetE = TagSet(community.founder, community, [tag], 'League')
    tagsetE.create()
    tagsetF = TagSet(community.founder, community, [tag], 'League')
    tagsetF.create()

    assert tagsetA.success
    assert tagsetB.success
    assert tagsetC.success
    assert tagsetD.success
    assert tagsetE.success
    assert not tagsetF.success
    assert len(community.tags) == 7

    #Check that we get all TagSets back
    response = requests.post("http://127.0.0.1:5000/tag_set/list", json={'Client': 'true', 'Active': 't'})
    assert response.status_code == 200

    data = response.json()
    pprint(data)
    assert len(data['Tag Sets']) == 5

def test_endpoint_community_get_tags():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True


    tag1 = Tag(community.founder, community)
    tag1.create()


    tag2 = Tag(community.founder, community)
    tag2.create()

    tagset = TagSet(community.founder, community, [tag1, tag2], 'League')
    tagset.create()

    tags = get_community_tags(community.name, sponsor)

    assert tags[0]

    # 2 tags above + tagset tag + the community tag
    assert len(tags[1]['Tags']) == 4

    #Check that all tags match what we have been tracking
    for x in tags[1]['Tags']:
        assert compare_comm_tag_to_dict(x, community.tags[x['id']])

def test_endpoint_community_get_members():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    member = User()
    member.register()

    future_admin = User()
    future_admin.register()
    
    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True

    # Member join
    assert community.join_via_request(member)
    assert community.join_via_request(future_admin)

    # Upgrade future admin user as admin
    assert community.manage(sponsor, [future_admin], "admin")
    assert community.get_member(future_admin).admin

    members = get_community_members(community.name, community.sponsor)

    assert members[0]

    assert len(members[1]['Members']) == 3

    for x in members[1]['Members']:
        assert compare_comm_user_to_dict(x, community.members[x['id']])

def test_community_sponsor_manage():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: mvp') == True

    member = User()
    member.register()

    future_sponsor = User()
    future_sponsor.register()

    #assert sponsor.add_to_group('patron: mvp') == True
    
    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True

    # Member join
    assert community.join_via_request(member)
    assert community.join_via_request(future_sponsor)

    # Try to remove sponsor as regular member
    assert not community.manage_sponsor(future_sponsor, 'Remove')
    # print(community.sponsor.to_dict())
    # print(sponsor.to_dict())
    # print(future_sponsor.to_dict())
    assert compare_users(community.sponsor, sponsor)
    
    # Remove sponsor as sponsor
    assert community.manage_sponsor(sponsor, 'Remove')
    assert community.sponsor == None

    # Add new sponsor, not a patron
    assert not community.manage_sponsor(future_sponsor, 'Add')
    assert community.sponsor == None

    # Add new sponsor who is now patron
    future_sponsor.verify_user()
    assert future_sponsor.add_to_group('patron: mvp') == True
    assert community.manage_sponsor(future_sponsor, 'Add')
    # print(community.sponsor)
    # print(future_sponsor)
    assert compare_users(community.sponsor, future_sponsor)


def test_community_sponsorless_tagset_create():
    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: rookie') == True

    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True

    # Remove sponsor as sponsor
    assert community.manage_sponsor(sponsor, 'Remove')
    assert community.sponsor == None

    # Create Tags
    tag = Tag(community.founder, community)
    tag.create()

    tagset = TagSet(community.founder, community, [tag], 'League')
    tagset.create()

    assert not tagset.success

def test_community_create_nonpatron():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == False
    
def test_community_create_patreon_limit():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('patron: rookie') == True

    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == True

    community = Community(sponsor, official=False, private=False, link=False)
    assert community.success == False

def test_community_gecko_tags():
    wipe_db()

    sponsor = User()
    sponsor.register()
    assert sponsor.success == True

    sponsor.verify_user()
    assert sponsor.add_to_group('admin') == True

    # Assert community IS created, sponsor is admin
    community = Community(sponsor, True, False, False)
    assert community.success == True
    
    # Should just have community tag
    assert len(community.tags) == 1

    code_dict = {'Gecko Code Desc': 'Code A desc', 'Gecko Code': 'DEADBEEF DEADBEEF\n'}

    # Add tag with admin
    tag = Tag(community.founder, community, 'Gecko Code', code_dict)
    tag.create()

    assert tag.active
    assert tag.type == 'Gecko Code'
    assert len(community.tags) == 2

    #==== Test getting Gecko Code back as client ====

    response = requests.post("http://127.0.0.1:5000/tag/list", json={'Client': 'true'})
    assert (response.status_code == 200)

    tag_dict = json.loads(response.text)

    print(tag_dict)

    for tag in tag_dict['Tags']:
        assert 'gecko_code' in tag.keys()

    #==== Test getting Gecko Code back as client [Only Code/competition] ====

    response = requests.post("http://127.0.0.1:5000/tag/list", json={'Client': 'true', 
                                                                     'Types': ['Competition', 'Gecko Code']})
    assert (response.status_code == 200)

    tag_dict = json.loads(response.text)

    print(tag_dict)

    for tag in tag_dict['Tags']:
        assert 'gecko_code' in tag.keys()

    assert len(tag_dict['Tags']) == 1

    #==== Test getting Gecko Code back as frontend (not client) ====

    response = requests.post("http://127.0.0.1:5000/tag/list")
    assert (response.status_code == 200)

    tag_dict = json.loads(response.text)

    print(tag_dict)

    for tag in tag_dict['Tags']:
        if tag['type'] == 'Gecko Code':
            assert 'gecko_code' in tag.keys()
        else:
            assert 'gecko_code' not in tag.keys()