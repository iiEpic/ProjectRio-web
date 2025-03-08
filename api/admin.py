from django.contrib import admin
from api.models import *


# Register your models here.
@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    pass


@admin.register(CharacterChemistry)
class CharacterChemistryAdmin(admin.ModelAdmin):
    pass


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunityUser)
class CommunityUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'community', 'role', 'status', 'date_joined']
    list_filter = ['community', 'status']
    search_fields = ['user']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'tag_type', 'date_created', 'last_modified']
    list_filter = ['tag_type']


@admin.register(TagSet)
class TagSetAdmin(admin.ModelAdmin):
    pass


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
