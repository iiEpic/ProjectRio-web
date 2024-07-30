import json
import secrets
from api import models
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def create_characters(self):
        f = open('./json/characters.json')
        character_list = json.load(f)["Characters"]

        for character in character_list:
            chemistry_table = models.ChemistryTable.objects.create(
                mario=character['Mario (0x3b)'],
                luigi=character['Luigi (0x3c)'],
                dk=character['DK (0x3d)'],
                diddy=character['Diddy (0x3e)'],
                peach=character['Peach (0x3f)'],
                daisy=character['Daisy (0x40)'],
                yoshi=character['Yoshi (0x41)'],
                baby_mario=character['Baby Mario (0x42)'],
                baby_luigi=character['Baby Luigi (0x43)'],
                bowser=character['Bowser (0x44)'],
                wario=character['Wario (0x45)'],
                waluigi=character['Waluigi (0x46)'],
                koopa_r=character['Koopa(R) (0x47)'],
                toad_r=character['Toad(R) (0x48)'],
                boo=character['Boo (0x49)'],
                toadette=character['Toadette (0x4a)'],
                shy_guy_r=character['Shy Guy(R) (0x4b)'],
                birdo=character['Birdo (0x4c)'],
                monty=character['Monty (0x4d)'],
                bowser_jr=character['Bowser Jr (0x4e)'],
                paratroopa_r=character['Paratroopa(R) (0x4f)'],
                pianta_b=character['Pianta(B) (0x50)'],
                pianta_r=character['Pianta(R) (0x51)'],
                pianta_y=character['Pianta(Y) (0x52)'],
                noki_b=character['Noki(B) (0x53)'],
                noki_r=character['Noki(R) (0x54)'],
                noki_g=character['Noki(G) (0x55)'],
                bro_h=character['Bro(H) (0x56)'],
                toadsworth=character['Toadsworth (0x57)'],
                toad_b=character['Toad(B) (0x58)'],
                toad_y=character['Toad(Y) (0x59)'],
                toad_g=character['Toad(G) (0x5a)'],
                toad_p=character['Toad(P) (0x5b)'],
                magikoopa_b=character['Magikoopa(B) (0x5c)'],
                magikoopa_r=character['Magikoopa(R) (0x5d)'],
                magikoopa_g=character['Magikoopa(G) (0x5e)'],
                magikoopa_y=character['Magikoopa(Y) (0x5f)'],
                king_boo=character['King Boo (0x60)'],
                petey=character['Petey (0x61)'],
                dixie=character['Dixie (0x62)'],
                goomba=character['Goomba (0x63)'],
                paragoomba=character['Paragoomba (0x64)'],
                koopa_g=character['Koopa(G) (0x65)'],
                paratroopa_g=character['Paratroopa(G) (0x66)'],
                shy_guy_b=character['Shy Guy(B) (0x67)'],
                shy_guy_y=character['Shy Guy(Y) (0x68)'],
                shy_guy_g=character['Shy Guy(G) (0x69)'],
                shy_guy_bk=character['Shy Guy(Bk) (0x6a)'],
                dry_bones_gy=character['Dry Bones(Gy) (0x6b)'],
                dry_bones_g=character['Dry Bones(G) (0x6c)'],
                dry_bones_r=character['Dry Bones(R) (0x6d)'],
                dry_bones_b=character['Dry Bones(B) (0x6e)'],
                bro_f=character['Bro(F) (0x6f)'],
                bro_b=character['Bro(B) (0x70)'],
            )

            character = models.Character.objects.create(
                chemistry_table=chemistry_table,
                name=character['Char Name'],
                starting_addr=character['Starting Addr'],
                curve_ball_speed=character['Curve Ball Speed (0x0)'],
                fast_ball_speed=character['Fast Ball Speed (0x1)'],
                curve=character['Curve (0x3)'],
                fielding_arm=character['Fielding Arm (righty:0,lefty:1) (0x26)'],
                batting_stance=character['Batting Stance (righty:0,lefty:1) (0x27)'],
                nice_contact_spot_size=character['Nice Contact Spot Size (0x28)'],
                perfect_contact_spot_size=character['Perfect Contact Spot Size (0x29)'],
                slap_hit_power=character['Slap Hit Power (0x2a)'],
                charge_hit_power=character['Charge Hit Power (0x2b)'],
                bunting=character['Bunting (0x2c)'],
                hit_trajectory_mpp=character['Hit trajectory (mid:0,pull:1,push:2) (0x2d)'],
                hit_trajectory_mhl=character['Hit trajectory (mid:0,high:1,low:2) (0x2e)'],
                speed=character['Speed (0x2f)'],
                throwing_arm=character['Throwing Arm (0x30)'],
                character_class=character['Character Class (balance:0,power:1,speed:2,technique:3) (0x31)'],
                weight=character['Weight (0x32)'],
                captain=character['Captain (true:1,false:0) (0x33)'],
                captain_star_hit_or_pitch=character['Captain Star Hit/Pitch (0x34)'],
                non_captain_star_swing=character['Non Captain Star Swing (1:pop fly,2:grounder,3:line drive) (0x35)'],
                non_captain_star_pitch=character['Non Captain Star Pitch (0x36)'],
                batting_stat_bar=character['Batting Stat Bar (0x37)'],
                pitching_stat_bar=character['Pitching Stat Bar (0x38)'],
                running_stat_bar=character['Running Stat Bar (0x39)'],
                fielding_stat_bar=character['Fielding Stat Bar (0x3a)'],
            )

    def create_default_tags(self):
        #     name els.CharField(max_length=32, unique=True)
        #     tag_type = models.CharField(max_length=16)
        #     desc = models.CharField(max_length=300)
        #     active = models.BooleanField(default=True)
        #     date_created = mod
        tags = [
            {
                'name': 'Ranked',
                'description': 'Tag for Ranked games',
                'tag_type': 'Global'
            },
            {
                'name': 'Unranked',
                'description': 'Tag for Unranked games',
                'tag_type': 'Global'
            },
            {
                'name': 'Superstar',
                'description': 'Tag for Stars On',
                'tag_type': 'Global'
            },
            {
                'name': 'Normal',
                'description': 'Tag for Normal games',
                'tag_type': 'Global'
            },
            {
                'name': 'Netplay',
                'description': 'Tag for Netplay games',
                'tag_type': 'Global'
            },
            {
                'name': 'Local',
                'description': 'Tag for Local games',
                'tag_type': 'Global'
            }
        ]

        for tag in tags:
            models.Tag.objects.get_or_create(**tag)

    def create_default_groups(self):
        groups = [
            {
                'name': 'Admin',
                'daily_limit': 0,
                'weekly_limit': 0,
                'sponsor_limit': 999
            },
            {
                'name': 'Developer',
                'daily_limit': 0,
                'weekly_limit': 0,
                'sponsor_limit': 999
            },
            {
                'name': 'Patron: Fan',
                'daily_limit': 0,
                'weekly_limit': 0,
                'sponsor_limit': 0
            },
            {
                'name': 'Patron: Rookie',
                'daily_limit': 0,
                'weekly_limit': 0,
                'sponsor_limit': 1
            },
            {
                'name': 'Patron: MVP',
                'daily_limit': 0,
                'weekly_limit': 0,
                'sponsor_limit': 5
            },
            {
                'name': 'Patron: Hall of Famer',
                'daily_limit': 0,
                'weekly_limit': 0,
                'sponsor_limit': 10
            },
            {
                'name': 'General',
                'daily_limit': 0,
                'weekly_limit': 0,
                'sponsor_limit': 0
            }
        ]
        for group in groups:
            models.UserGroup.objects.get_or_create(**group)

    def create_official_infrastructure(self):
        admin_user = self.create_admin_users()
        self.create_official_comms(admin_user)

    def create_admin_users(self):
        admin_backend_user = get_user_model().objects.filter(username='ProjectRio').first()
        if admin_backend_user is None:
            admin_backend_user = get_user_model().objects.create(
                username='ProjectRio',
                email='projectrio.dev@gmail.com',
                password=secrets.token_urlsafe(32)
            )
        admin_user = models.RioUser.objects.filter(user=admin_backend_user).first()
        if admin_user is None:
            admin_user = models.RioUser.objects.create(
                user=admin_backend_user,
                verified=True,
                active_url=None
            )

        # Get admin group
        user_group = models.UserGroup.objects.filter(name__iexact='admin').first()

        # Add admin user to group
        admin_user.user_group.add(user_group)
        admin_user.save()

        return admin_user

    def create_official_comms(self, admin_user):
        new_comm = models.Community.objects.filter(name='ProjectRio').first()
        if new_comm is None:
            new_comm = models.Community.objects.create(
                name='ProjectRio',
                sponsor=admin_user,
                community_type='Official',
                private=False,
                active_tag_set_limit=5,
                active_url=secrets.token_urlsafe(32),
                description='Official community of ProjectRio'
            )

        # === Create CommunityUser (admin)
        comm_user = models.CommunityUser.objects.filter(user=admin_user, community=new_comm).first()
        if comm_user is None:
            models.CommunityUser.objects.get_or_create(
                user=admin_user,
                community=new_comm,
                admin=True,
                invited=False,
                active=True
            )

        # === Create Community Tag ===
        models.Tag.objects.get_or_create(
            name=new_comm.name,
            tag_type='Community',
            description=f"Community tag for {new_comm.name}"
        )

    def handle(self, *args, **options):
        self.create_characters()
        self.create_default_tags()
        self.create_default_groups()
        self.create_official_infrastructure()
