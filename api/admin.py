from django.contrib import admin
from api.models import *


# Register your models here.
@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'sponsor_limit', 'daily_limit', 'weekly_limit']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'private', 'verified', 'get_groups']

    def get_groups(self, object):
        return [i for i in object.user_group.all()]
    get_groups.short_description = 'Groups'


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    pass


@admin.register(CharacterChemistry)
class CharacterChemistryAdmin(admin.ModelAdmin):
    pass


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    pass


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_permissions']
    filter_horizontal = ['permissions']

    def get_permissions(self, object):
        return [i.name for i in object.permissions.all()]
    get_permissions.short_description = "Permissions"


@admin.register(CommunityUser)
class CommunityUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'community', 'role', 'status', 'date_joined']
    list_filter = ['community', 'status']
    search_fields = ['user']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'community', 'tag_type', 'date_created', 'last_modified']
    list_filter = ['tag_type']


@admin.register(TagSet)
class TagSetAdmin(admin.ModelAdmin):
    list_display = ['name', 'community', 'tagset_type', 'start_date', 'end_date']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(GameRoster)
class GameRosterAdmin(admin.ModelAdmin):
    pass


@admin.register(GameEventSummary)
class GameEventSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(Ladder)
class LadderAdmin(admin.ModelAdmin):
    pass


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass
