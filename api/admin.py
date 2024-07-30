from django.contrib import admin
from api.models import *


# Register your models here.
@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ['token', 'get_user', 'pings_daily', 'pings_weekly', 'total_pings', 'last_ping_date', 'date_created']

    @admin.display(description='User')
    def get_user(self, object):
        return object.token.user


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    pass


@admin.register(CharacterGameSummary)
class CharacterGameSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(CharacterPositionSummary)
class CharacterPositionSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(ChemistryTable)
class ChemistryTableAdmin(admin.ModelAdmin):
    pass


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunityUser)
class CommunityUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'community', 'admin', 'invited', 'active', 'banned', 'date_joined']
    list_filter = ['user', 'community']


@admin.register(ContactSummary)
class ContactSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(FieldingSummary)
class FieldingSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(GameHistory)
class GameHistoryAdmin(admin.ModelAdmin):
    pass


@admin.register(GeckoCodeTag)
class GeckoCodeTagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ladder)
class LadderAdmin(admin.ModelAdmin):
    pass


@admin.register(OngoingGame)
class OngoingGameAdmin(admin.ModelAdmin):
    pass


@admin.register(PitchSummary)
class PitchSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(RioUser)
class RioUserAdmin(admin.ModelAdmin):
    filter_horizontal = ['user_group']


@admin.register(Runner)
class RunnerAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass


@admin.register(TagSet)
class TagSetAdmin(admin.ModelAdmin):
    pass


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    pass
